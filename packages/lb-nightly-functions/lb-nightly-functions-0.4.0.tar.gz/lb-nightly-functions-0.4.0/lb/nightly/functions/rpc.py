###############################################################################
# (c) Copyright 2020-2022 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""
Entry point functions for nightly build operations.
"""
import json
import os
import pathlib
import socket
from functools import wraps
from pathlib import Path
from subprocess import STDOUT, check_output

import archspec.cpu
from lb.nightly.configuration import (
    DataProject,
    Package,
    Project,
    get,
    lbnightly_settings,
    service_config,
)
from lb.nightly.db import connect as db
from lb.nightly.db.utils import LockTakenError
from lb.nightly.utils import Repository

from .common import (
    Report,
    build_env,
    compute_env,
    download_and_unzip,
    get_build_method,
    wait_for_deployment_dirs,
)


def checkout(project_id: str, worker_task_id: str, gitlab_token=None):
    from .checkout import git, notify_gitlab, update_nightly_git_archive

    conf = service_config()

    gitlab_token = (
        gitlab_token
        or conf.get("gitlab", {}).get("token")
        or os.environ.get("GITLAB_TOKEN")
    )

    project = get(project_id)
    if not isinstance(project, (Project, Package)):
        raise ValueError(
            f"project_id {project_id} does not identify a nightly builds Project instance"
        )

    artifact_name = project.artifacts("checkout")

    report = Report("rpc_checkout_script")
    artifacts_repo = (
        Repository.connect(conf["artifacts"]["uri"]) if "artifacts" in conf else None
    )
    if not artifacts_repo:
        report.warning("artifacts repository not configured: no publishing")

    logs_repo = Repository.connect(conf["logs"]["uri"]) if "logs" in conf else None
    if not logs_repo:
        report.warning("logs repository not configured: no publishing")

    # if the artifact already exists and if we can reuse the checkout
    # summary we are done, otherwise we can continue
    if (
        artifacts_repo
        and artifacts_repo.exist(artifact_name)
        and db().reuse_artifact(project, artifact_name)
    ):
        return report

    db().checkout_start(project, worker_task_id)

    # checkout the project
    report = git(project)

    # record the working directory
    report.cwd = os.getcwd()

    if gitlab_token:
        if isinstance(project, DataProject):
            for pkg, pkg_report in zip(project.packages, report.packages):
                notify_gitlab(pkg, pkg_report, gitlab_token)
        else:
            report = notify_gitlab(project, report, gitlab_token)

    # gitlab archive and dependencies are not possible for data projects
    if not isinstance(project, (DataProject, Package)):
        try:
            report = update_nightly_git_archive(project, report)
        except Exception as err:
            report.warning(f"failed to update Git archive: {err}")

        # resolve and update dependencies
        db().set_dependencies(project)

    if isinstance(project, Package):
        dir_to_pack = os.path.join(project.container.name, project.name)
    else:
        dir_to_pack = project.name
    archive_name = os.path.basename(project.artifacts("checkout"))

    report.info(f"packing {dir_to_pack} into {archive_name}")
    report.log(
        "stdout",
        "debug",
        check_output(
            [
                "zip",
                "-r",
                "-y",
                archive_name,
                dir_to_pack,
            ],
            stderr=STDOUT,
        ).decode(),
    )

    report.info(f"adding logs to {archive_name}")

    log_dir = pathlib.Path(dir_to_pack) / ".logs" / "checkout"
    os.makedirs(log_dir)
    with open(log_dir / "report.json", "w") as f:
        json.dump(report.to_dict(), f, indent=2)
    with open(log_dir / "report.md", "w") as f:
        f.write(report.md())

    report.log(
        "stdout",
        "debug",
        check_output(
            ["zip", "-r", archive_name, log_dir],
            stderr=STDOUT,
        ).decode(),
    )

    if artifacts_repo:
        if not artifacts_repo.push(open(archive_name, "rb"), artifact_name):
            raise RuntimeError(
                f"failed to upload {artifact_name} to artifacts repository"
            )

    if logs_repo:
        if not logs_repo.push(
            open(log_dir / "report.json", "rb"),
            f"{artifact_name}-report.json",
        ):
            raise RuntimeError(
                f"failed to upload {artifact_name}-report.json to logs repository"
            )

    db().checkout_complete(project, artifact_name, report, worker_task_id)


def nightly_task(task):
    @wraps(task)
    def wrapper(project_id: str, platform: str, worker_task_id: str, *args, **kwargs):
        project = get(project_id)
        if not isinstance(project, Project):
            raise ValueError(
                f"project_id {project_id} does not identify a nightly builds "
                "Project instance"
            )

        env = compute_env(
            project,
            build_env(project, platform),
            kwargs.get("override_env"),
        )
        project.env = [f"{k}={v}" for k, v in env.items()]

        if "CMAKE_USE_CCACHE" not in project.slot.cache_entries:
            project.slot.cache_entries["CMAKE_USE_CCACHE"] = True

        hash = project.hash(platform)
        artifact_name = str(
            Path(task.__name__) / project.name / hash[:2] / (hash + ".zip")
        )
        build_artifact_name = (
            str(Path("build") / project.name / hash[:2] / (hash + ".zip"))
            if task.__name__ == "test"
            else None
        )
        conf = service_config()
        repo = Repository.connect()
        rpc_report = Report(f"rpc_{task.__name__}_script")

        if repo.exist(artifact_name):
            # if we are here it means that artifact is present, but the summary
            # is not available in the database, so we just update it and return
            rpc_report.info(
                f"{task.__name__} artifact for {project} and {platform}"
                " found in cache. Updating the summary in the database"
            )
            if db().reuse_artifact(
                project,
                artifact_name,
                platform,
                task.__name__,
            ):
                rpc_report.info(
                    f"Summary for the {task.__name__} artifact for {project} and {platform}"
                    " updated in the database"
                )
            else:
                rpc_report.error(
                    f"Summary for the {task.__name__} artifact for {project} and {platform}"
                    " not found in the database"
                )
            return {"script": rpc_report}

        else:
            try:
                with db().lock(
                    artifact_name.replace("/", ":"), info={"artifact": artifact_name}
                ):
                    task(
                        project,
                        platform,
                        env,
                        worker_task_id,
                        repo,
                        conf,
                        rpc_report,
                        artifact_name,
                        build_artifact_name=build_artifact_name,
                    )
            except LockTakenError:
                rpc_report.warning(
                    f"Someone else {task.__name__}ing {project} on {platform} (artifact: {artifact_name}). "
                    "Exiting"
                )
                return {"script": rpc_report}

    return wrapper


@nightly_task
def build(
    project: Project,
    platform: str,
    env: dict,
    worker_task_id: str,
    repo: Repository,
    conf: dict,
    rpc_report: Report,
    artifact_name: str,
    **kwargs,
):

    assert download_and_unzip(
        repo, project.artifacts("checkout")
    ), f"could not get checkout artifacts for {project.id()}"
    wait_for_deployment_dirs(project, platform, "build")
    db().build_start(project, platform, worker_task_id)
    report, build_logs = get_build_method(project)(project).build(
        jobs=int(os.environ.get("LBN_BUILD_JOBS") or "0") or os.cpu_count() or 1,
        env=env,
        worker_task_id=worker_task_id,
        cache_entries=project.slot.cache_entries,
        # if not in release builds (i.e. no_patch = False) allow missing artifacts
        relaxed_install=not project.slot.no_patch,
    )
    archive_name = os.path.basename(artifact_name)
    report["script"].info(f"packing {project.name} into {archive_name}")
    report["script"].log(
        "stdout",
        "debug",
        check_output(
            [
                "zip",
                "-r",
                "-y",
                archive_name,
                project.name,
                "-i",
                f"{project.name}/build/*",
                f"{project.name}/InstallArea/*",
            ],
            stderr=STDOUT,
        ).decode(),
    )

    report["script"].info(f"adding logs to {archive_name}")

    log_dir = pathlib.Path(project.name) / ".logs" / platform / "build"
    os.makedirs(log_dir, exist_ok=True)
    with open(log_dir / "report.md", "w") as f:
        for step in report.values():
            f.write(step.md())
            f.write("\n")

    jreport = {}
    from .build_log import generate_build_report

    try:
        completed = report["install"].completed
    except AttributeError:
        try:
            completed = report["build"].completed
        except AttributeError:
            completed = report["configure"].completed
    retcodes = set()
    for rep in report.values():
        try:
            retcodes.add(rep.returncode)
        except AttributeError:
            pass

    for record in rpc_report.records:
        report["script"].records.append(record)

    reports_json = {k: v.to_dict() for k, v in report.items()}
    for val in reports_json.values():
        try:
            val["stdout"] = val["stdout"].decode(errors="surrogateescape")
            val["stderr"] = val["stderr"].decode(errors="surrogateescape")
        except KeyError:
            pass

    jreport = generate_build_report(
        build_logs=build_logs,
        proj_build_root=project.name,
        exceptions={
            "warning": project.slot.warning_exceptions,
            "error": project.slot.error_exceptions,
        },
        extra_info={
            "project": project.name,
            "version": project.version,
            "slot": project.slot.name,
            "slot_build_id": project.slot.build_id,
            "host": socket.gethostname(),
            "platform": platform,
            "started": report["configure"].started,
            "completed": completed,
            "retcode": max(retcodes),
            "environment": env,
            "cpu": archspec.cpu.detect.raw_info_dictionary(),
            "reports": reports_json,
        },
    )
    with open(log_dir / "report.json", "w") as f:
        json.dump(jreport, f, indent=2)

    report["script"].log(
        "stdout",
        "debug",
        check_output(
            ["zip", "-r", "-y", archive_name, log_dir], stderr=STDOUT
        ).decode(),
    )

    assert repo.push(
        open(archive_name, "rb"), artifact_name
    ), "failed to upload artifacts"

    if "logs" in conf:
        logs_repo = Repository.connect(conf["logs"]["uri"])
        assert logs_repo.push(
            open(log_dir / "report.json", "rb"),
            artifact_name + "-report.json",
        ), "failed to upload log"

    else:
        report["script"].warning("logs repository not configured: no publishing")

    db().build_complete(
        project,
        platform,
        artifact_name,
        jreport,
        worker_task_id,
    )
    return report


@nightly_task
def test(
    project: Project,
    platform: str,
    env: dict,
    worker_task_id: str,
    repo: Repository,
    conf: dict,
    rpc_report: Report,
    artifact_name: str,
    **kwargs,
):

    assert download_and_unzip(
        repo, project.artifacts("checkout")
    ), f"could not get checkout artifacts for {project.id()}"
    assert download_and_unzip(
        repo, kwargs.get("build_artifact_name", "")
    ), f"could not get build artifacts {project.id()} and {platform}"
    wait_for_deployment_dirs(project, platform, "test")

    try:
        krb_auth = (
            lbnightly_settings()["kerberos"]["user"],
            lbnightly_settings()["kerberos"]["keytab"],
        )
    except KeyError:
        rpc_report.warning("Missing kerberos credentials. Some tests may fail.")
        krb_auth = None

    db().tests_start(project, platform, worker_task_id)

    report = get_build_method(project)(project).test(
        env=env,
        krb_auth=krb_auth,
        worker_task_id=worker_task_id,
    )

    reports = {"report": report, "results": {}}

    from xml.etree import ElementTree as ET

    try:
        xml = ET.parse(next(pathlib.Path(".").glob("**/Test.xml")))
        status_translation = {
            "passed": "PASS",
            "failed": "FAIL",
            "skipped": "SKIPPED",
            "notrun": "SKIPPED",
            "error": "ERROR",
            "untested": "UNTESTED",
        }
        from itertools import groupby

        tests = sorted(
            xml.findall("./Testing/Test[@Status]"),
            key=lambda test: test.attrib["Status"],
        )
        summary = {
            status_translation[key]: sorted(test.find("Name").text for test in group)
            for key, group in groupby(tests, key=lambda test: test.attrib["Status"])
        }
        reports["results"] = summary
    except StopIteration:
        report["script"].error("failed to parse Test.xml (file is missing)")

    archive_name = os.path.basename(artifact_name)
    report["script"].info(f"packing {project.name} into {archive_name}")
    report["script"].info(f"adding logs to {archive_name}")

    log_dir = pathlib.Path(project.name) / ".logs" / platform / "test"
    os.makedirs(log_dir, exist_ok=True)
    for step in report.keys():
        with open(log_dir / "report.md", "a") as f:
            f.write(f"{report[step].md()}\n")

    for record in rpc_report.records:
        report["script"].records.append(record)

    reports_json = {k: v.to_dict() for k, v in report.items()}
    for val in reports_json.values():
        try:
            val["stdout"] = val["stdout"].decode(errors="surrogateescape")
            val["stderr"] = val["stderr"].decode(errors="surrogateescape")
        except KeyError:
            pass

    with open(log_dir / "report.json", "w") as f:
        json.dump(reports_json, f, indent=2)

    report["script"].log(
        "stdout",
        "debug",
        check_output(
            [
                "zip",
                "-r",
                archive_name,
                log_dir,
            ],
            stderr=STDOUT,
        ).decode(),
    )

    assert repo.push(
        open(archive_name, "rb"), artifact_name
    ), "failed to upload artifacts"

    if "logs" in conf:
        logs_repo = Repository.connect(conf["logs"]["uri"])
        assert logs_repo.push(
            open(log_dir / "report.json", "rb"),
            artifact_name + "-report.json",
        ), "failed to upload log"
        try:
            with open(f"{project.name}/build/Testing/TAG") as tagfile:
                assert logs_repo.push(
                    open(
                        f"{project.name}/build/Testing/{tagfile.readline().strip()}/Test.xml",
                        "rb",
                    ),
                    kwargs.get("build_artifact_name", "") + "-Test.xml",
                ), "failed to upload Test.xml (pushing to repo failed)"
        except FileNotFoundError:
            report["script"].error("failed to upload Test.xml (file is missing)")

    else:
        report["script"].warning("logs repository not configured: no publishing")

    db().tests_complete(project, platform, artifact_name, reports, worker_task_id)

    return report


if __name__ == "__main__":  # pragma: no cover
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG)
    globals()[sys.argv[1]](*sys.argv[2:])
