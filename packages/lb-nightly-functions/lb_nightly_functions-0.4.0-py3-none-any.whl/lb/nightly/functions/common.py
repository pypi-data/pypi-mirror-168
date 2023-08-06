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
import asyncio
import json
import logging
import os
import re
import socket
from collections import namedtuple
from datetime import datetime, timedelta, timezone
from pathlib import Path
from shutil import copyfileobj
from subprocess import CalledProcessError, run
from tempfile import NamedTemporaryFile
from time import sleep
from typing import Optional
from zlib import decompress

from git import GitCommandError
from lb.nightly.configuration import DataProject, Package, Project, lbnightly_settings

from . import CMAKE_DIR, DATA_DIR

TIME_BETWEEN_DEPLOYMENT_CHECKS = timedelta(minutes=1)
MAX_TIME_WAITING_FOR_DEPLOYMENT = timedelta(hours=1)


class Report:
    """
    Class used to collect reports.

    Record messages and forward them to a logger.

    Apart from normal logging levels, accept extra type of messages, like
    ``git_error``.
    """

    def __init__(self, logger=__name__):
        self.logger = logging.getLogger(logger)
        self.records = []

    def log(self, type, level, fmt, args=None):
        record = {"type": type, "level": level, "text": (fmt % args if args else fmt)}
        if type in ("error", "warning") and f"{type}:" not in record["text"]:
            record["text"] = "{}: {}".format(type, record["text"])
        self.records.append(record)
        getattr(self.logger, level)(fmt, *(() if args is None else args))

    def debug(self, fmt, *args):
        self.log("debug", "debug", fmt, args)

    def info(self, fmt, *args):
        self.log("info", "info", fmt, args)

    def warning(self, fmt, *args):
        self.log("warning", "warning", fmt, args)

    warn = warning

    def error(self, fmt, *args):
        self.log("error", "error", fmt, args)

    def git_error(self, msg, err: GitCommandError):
        """
        Special handling for GitCommandError
        """
        self.warning("%s: GitCommand status %s", msg, err.status)
        # FIXME: this is very much subject to the internal details of GitCommandError
        self.log("command", "debug", "> %s", (err._cmdline,))
        if "'" in err.stdout:
            self.log(
                "stdout", "debug", err.stdout[err.stdout.index("'") + 1 : -1].rstrip()
            )
        if "'" in err.stderr:
            self.log(
                "stderr", "debug", err.stderr[err.stderr.index("'") + 1 : -1].rstrip()
            )

    def md(self):
        """
        Format as markdown.
        """
        out = []
        if hasattr(self, "project"):
            out.append("# {name}/{version}".format(**self.project))
        for r in self.records:
            lines = r["text"].splitlines()
            if r["type"] in ("stdout", "stderr", "command"):
                out.append("  ```")
                out.extend("  " + l for l in lines)
                out.append("  ```")
            else:
                out.append("- " + lines.pop(0))
                out.extend("  " + l for l in lines)
        if hasattr(self, "packages"):
            out.extend(pkg.md() for pkg in self.packages)
        return "\n".join(out)

    def __str__(self):
        out = []
        if hasattr(self, "project"):
            out.append("{name}/{version}".format(**self.project))
            out.append("-" * len(out[-1]))
            out.append("")
        out.extend(r["text"] for r in self.records)
        if hasattr(self, "packages"):
            out.extend(str(pkg) for pkg in self.packages)
        return "\n".join(out)

    def to_dict(self):
        from copy import deepcopy

        data = deepcopy(self.__dict__)
        data["logger"] = self.logger.name
        if "packages" in data:
            data["packages"] = [pkg.to_dict() for pkg in data["packages"]]

        return data


def ensure_dir(path, rep: Report):
    """
    Make sure that a directory exist, creating it
    and passing a warning to Report object if dir does not exist.
    """
    if not os.path.exists(path):
        rep.warning(f"directory {path} is missing, I create it")
        os.makedirs(path)


def find_path(name, search_path=None):
    """
    Look for a file or directory in a search path.

    If the search path is not specified, the concatenation of CMTPROJECTPATH
    and CMAKE_PREFIX_PATH is used.

    >>> find_path('true', ['/usr/local/bin', '/bin'])
    '/bin/true'
    >>> print(find_path('cannot_find_me', []))
    None
    """
    from os import environ, pathsep
    from os.path import exists, join

    if search_path is None:
        search_path = environ.get("CMAKE_PREFIX_PATH", "").split(pathsep) + environ.get(
            "CMTPROJECTPATH", ""
        ).split(pathsep)

    try:
        return next(
            join(path, name) for path in search_path if exists(join(path, name))
        )
    except StopIteration:
        logging.warning("%s not found in %r", name, search_path)
    return None


def get_build_method(project=None):
    """
    Helper function to get a build method for a project.

    The method is looked up in the following order: build_tool property of a project,
    build_tool property of a slot owning the project, the default build method (cmake).

    If a method is retrieved via build_tool string property, it must be defined in
    lb.nightly.functions.build.
    """
    import lb.nightly.functions.build as build_methods

    try:
        method = project.build_tool or project.slot.build_tool
        return getattr(build_methods, method)
    except (AttributeError, TypeError):
        return build_methods.cmake


def safe_dict(mydict):
    """Helper to return the dictionary without sensitive data
    To be used e.g. to remove secret environment variables.
    >>> d={"PASSWORD": "my_secret_pass", "PASS": "asd", "USER": "me",\
    "KEY": "asd", "TOKEN": "asd", "PRIVATE": "Asd", "HOME": "Asd",\
    "SHA": "asd", "KRB5CCNAME": "FILE:/tmp/user_123"}
    >>> safe_dict(d)
    {}
    """
    return {
        k: v
        for k, v in mydict.items()
        if all(
            s not in k.upper()
            for s in [
                "PASS",
                "USER",
                "KEY",
                "TOKEN",
                "PRIVATE",
                "HOME",
                "SHA",
                "KRB5",
            ]
        )
    }


def singularity_run(
    cmd: list,
    env: Optional[dict] = None,
    cwd: str = os.curdir,
    task: Optional[dict] = None,
    krb_auth: Optional[tuple] = None,
):
    s_env = safe_dict(env)

    # specify workspace in container
    workspace_singularity = pwd = "/workspace"
    if cwd != os.getcwd():
        cwd = os.path.join(workspace_singularity, cwd)
        pwd = cwd

    if krb_auth:
        krb_token = NamedTemporaryFile()
        s_env["KRB5CCNAME"] = f"FILE:{krb_token.name}"

        class KerberosAuthenticationError(Exception):
            pass

        try:
            run(
                [
                    "/usr/bin/kinit",
                    "-c",
                    krb_token.name,
                    "-k",
                    "-t",
                    krb_auth[1],
                    krb_auth[0],
                ],
                check=True,
            )
        except (CalledProcessError, IndexError):
            raise KerberosAuthenticationError(
                "Could not authenticate with provided credentials"
            )

    # stub of the msg to send to opensearch
    log_body = {
        "host": socket.gethostname(),
        "command": cmd,
        "cwd": cwd,
        "task": task.get("task"),
        "project": task.get("project"),
        "platform": task.get("platform"),
        "worker_task_id": task.get("worker_task_id"),
        "log": f"Running command: {cmd} with env: {safe_dict(s_env)}",
        "@timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f"),
    }

    if "TASK_LOGFILE" in env:
        with open(env.get("TASK_LOGFILE"), "a") as logfile:
            logfile.write(json.dumps(log_body) + "\n")

    # to collect the build messages we communicate through the UNIX socket
    from hashlib import sha256

    hash = sha256()
    hash.update(f"{cmd} {task} {cwd}".encode())
    os.environ["LB_WRAPCMD_SOCKET"] = s_env["LB_WRAPCMD_SOCKET"] = os.path.join(
        "/tmp", hash.hexdigest()[:32]
    )

    Result = namedtuple(
        "Result",
        [
            "returncode",
            "stdout",
            "stderr",
            "args",
            "build_logs",
        ],
    )

    try:

        build_logs = {}

        base_cmd = ["singularity", "exec"]
        base_cmd += ["--bind=/cvmfs"]
        base_cmd += [f"--bind={os.getcwd()}:{workspace_singularity}"]
        if env.get("CONDA_ENV"):
            base_cmd += [f"--bind={env.get('CONDA_ENV')}"]
        if env.get("NIGHTLIES_CACHE"):
            base_cmd += [f"--bind={env.get('NIGHTLIES_CACHE')}"]
        base_cmd += [f"--pwd={pwd}"]
        base_cmd += ["--cleanenv"]
        for key, value in s_env.items():
            base_cmd += [f"--env={key}={value}"]
        try:
            base_cmd += [env["SINGULARITY_ROOT"]]
        except KeyError:
            raise RuntimeError("Could not find the CernVM image")

        singularity_cmd = base_cmd + cmd

        async def _stream_to_file(stream):
            output = b""
            with open(env.get("TASK_LOGFILE"), "a", buffering=512) as f:
                while line := await stream.readline():
                    output += line
                    line = line.decode(errors="surrogateescape")
                    f.write(
                        json.dumps(
                            dict(
                                log_body,
                                **{
                                    "log": line.rstrip(),
                                    "@timestamp": datetime.now(timezone.utc).strftime(
                                        "%Y-%m-%dT%H:%M:%S.%f"
                                    ),
                                },
                            )
                        )
                        + "\n"
                    )
            return output

        async def run_in_singularity(cmd):
            process = await asyncio.create_subprocess_exec(
                *cmd,
                limit=1024 * 128,  # default is 64kb which is not enough for eg G4
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            streamers = []
            if "TASK_LOGFILE" in env:
                streamers = [
                    _stream_to_file(process.stdout),
                    _stream_to_file(process.stderr),
                ]
            aresults = await asyncio.gather(
                *streamers,
                process.wait(),
            )
            try:
                return aresults[0], aresults[1], aresults[2]
            except IndexError:
                return b"", b"", aresults[0]

        server_address = os.environ["LB_WRAPCMD_SOCKET"]
        try:
            os.unlink(server_address)
        except OSError:
            if os.path.exists(server_address):
                raise

        async def _receive(reader, writer):
            buffer = b""
            while True:
                msg = await reader.read(4096)
                if msg:
                    buffer += msg
                else:
                    break
            data = json.loads(decompress(buffer))
            build_logs.setdefault(data.pop("subdir"), {}).setdefault(
                data.pop("target"), []
            ).append(data)

        async def read_socket(server_address):
            server = await asyncio.start_unix_server(
                _receive,
                server_address,
            )
            async with server:
                try:
                    await server.serve_forever()
                except asyncio.exceptions.CancelledError:
                    pass

        async def main_get_read(cmd, server_address):
            _read_sock = asyncio.create_task(read_socket(server_address))
            _read_singularity = asyncio.create_task(run_in_singularity(cmd))
            done, pending = await asyncio.wait(
                [_read_sock, _read_singularity],
                return_when=asyncio.FIRST_COMPLETED,
                timeout=60 * 60 * 24,
            )
            retcode = 1  # will be overwritten
            for _task in done:
                if _task is _read_singularity:
                    stdout, stderr, retcode = _task.result()
                    _read_sock.cancel()
                    try:
                        await _read_sock
                    except asyncio.CancelledError:
                        pass
            return stdout, stderr, retcode

        stdout, stderr, retcode = asyncio.run(
            main_get_read(
                singularity_cmd,
                server_address,
            )
        )

    finally:
        try:
            os.unlink(server_address)
        except OSError:
            pass
        try:
            del os.environ["LB_WRAPCMD_SOCKET"]
        except KeyError:
            pass
        try:
            krb_token.close()
        except NameError:
            pass
    return Result(
        stdout=stdout,
        returncode=retcode,
        stderr=stderr,
        args=cmd,
        build_logs=build_logs,
    )


async def write_to_socket(socket_name, message):
    _, writer = await asyncio.open_unix_connection(socket_name)
    writer.write(message)
    await writer.drain()
    writer.close()
    await writer.wait_closed()


def lb_wrapcmd():
    """
    The script to be used in CMake launcher rules.

    A launcher rule defined as
    set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE "lb-wrapcmd <CMAKE_CURRENT_BINARY_DIR> <TARGET_NAME>")

    Output for each compile command is sent to the socket
    (name taken from LB_WRAPCMD_SOCKET env variable or built as:
    <CMAKE_CURRENT_BINARY_DIR>/1234-<TARGET_NAME>-abc-build.log)
    """
    import sys
    from argparse import REMAINDER, ArgumentParser
    from shutil import which
    from time import time
    from zlib import compress

    parser = ArgumentParser()
    parser.add_argument("log_dir", help="CMAKE_CURRENT_BINARY_DIR")
    parser.add_argument("target", help="TARGET_NAME")
    parser.add_argument("wrap_cmd", nargs=REMAINDER, help="wrapped command")
    args = parser.parse_args()

    with NamedTemporaryFile() as statistics_file:
        time_cmd = [
            which("time"),
            "-f",
            '{"duration": "%E", "maxresident": "%M", "avgresident": "%t", "cpupercentage": "%P"}',
            "-o",
            statistics_file.name,
        ]
        started = time()
        result = run(time_cmd + args.wrap_cmd, capture_output=True)
        completed = time()
        sys.stdout.buffer.write(result.stdout)
        sys.stderr.buffer.write(result.stderr)

        if "LB_WRAPCMD_SOCKET" in os.environ:
            server_address = os.environ["LB_WRAPCMD_SOCKET"]

            output = {
                "subdir": "/".join(args.log_dir.split("/")[4:]) or "ROOT_DIR",
                "target": args.target,
                "cmd": args.wrap_cmd,
                "stdout": "",
                "stderr": "",
                "returncode": result.returncode,
                "started": started,
                "completed": completed,
            }
            statistics_file.seek(0)
            with open(statistics_file.name, "r") as f:
                statistics = json.loads(f.read())
            output.update(statistics)

            if args.wrap_cmd[0] != "cat":
                output["stdout"] = result.stdout.decode(errors="surrogateescape")
                output["stderr"] = result.stderr.decode(errors="surrogateescape")

            asyncio.run(
                write_to_socket(server_address, compress(json.dumps(output).encode()))
            )

    return result.returncode


def download_and_unzip(repo, artifact):
    """
    Helper function to download the artifact
    and unzip it in the current directory.

    :param repo: ArtifactsRepository object to get the artifact from
    :param artifact: the value returned by the `artifacts`
    method of the Project.

    Returns True if succeded.
    """
    try:
        with NamedTemporaryFile() as lp:
            with repo.pull(artifact) as remote:
                copyfileobj(remote, lp)
            lp.seek(0)
            return not run(["unzip", "-o", lp.name], check=True).returncode
    except Exception:
        return False


def create_project_makefile(dest, overwrite=False):
    """Write the generic Makefile for CMT projects.
    @param dest: the name of the destination file
    @param overwrite: flag to decide if an already present file has to be kept
                      or not (default is False)
    """
    import logging

    if overwrite or not os.path.exists(dest):
        logging.debug("Creating '%s'", dest)
        with open(dest, "w") as f:
            f.write(
                "DEVTOOLS_DATADIR := {0}\n"
                "include $(DEVTOOLS_DATADIR)/Makefile-common.mk\n".format(DATA_DIR)
            )
        return True
    return False


def create_toolchain_file(dest, overwrite=False):
    """Write the generic toolchain.cmake file needed by CMake-based projects.
    @param dest: destination filename
    @param overwrite: flag to decide if an already present file has to be kept
                      or not (default is False)
    """
    import logging

    if overwrite or not os.path.exists(dest):
        logging.debug("Creating '%s'", dest)
        with open(dest, "w") as f:
            f.write("include({0})\n".format(os.path.join(DATA_DIR, "toolchain.cmake")))
        return True
    return False


def create_git_ignore(dest, overwrite=False, extra=None, selfignore=True):
    """Write a generic .gitignore file, useful for git repositories.
    @param dest: destination filename
    @param overwrite: flag to decide if an already present file has to be kept
                      or not (default is False)
    @param extra: list of extra patterns to add
    @param selfignore: if the .gitignore should include itself
    """
    import logging

    if overwrite or not os.path.exists(dest):
        logging.debug("Creating '%s'", dest)
        patterns = [
            "/InstallArea/",
            "/build.*/",
            "*.pyc",
            "*~",
            ".*.swp",
            "/.clang-format",
        ]
        if selfignore:
            patterns.insert(0, "/.gitignore")  # I like it as first entry
        if extra:
            patterns.extend(extra)

        with open(dest, "w") as f:
            f.write("\n".join(patterns))
            f.write("\n")
        return True
    return False


def create_clang_format(dest, overwrite=False):
    """Add `.clang-format` file.
    @param dest: destination filename
    @param overwrite: flag to decide if an already present file has to be kept
                      or not (default is False)
    """
    import logging

    if overwrite or not os.path.exists(dest):
        logging.debug("Creating '%s'", dest)
        with open(dest, "w") as f:
            f.writelines(open(os.path.join(DATA_DIR, "default.clang-format")))
        return True
    return False


def init_project(path, overwrite=False):
    """
    Initialize the sources for an LHCb project for building.

    Create the (generic) special files required for building LHCb/Gaudi
    projects.

    @param path: path to the root directory of the project
    @param overwrite: whether existing files should be overwritten, set it to
                      True to overwrite all of them or to a list of filenames
    """
    extraignore = []
    factories = [
        ("Makefile", create_project_makefile),
        ("toolchain.cmake", create_toolchain_file),
        (".clang-format", create_clang_format),
        (
            ".gitignore",
            lambda dest, overwrite: create_git_ignore(dest, overwrite, extraignore),
        ),
    ]

    # handle the possible values of overwrite to always have a set of names
    if overwrite in (False, None):
        overwrite = set()
    elif overwrite is True:
        overwrite = set(f[0] for f in factories)
    elif isinstance(overwrite, str):
        overwrite = set([overwrite])
    else:
        overwrite = set(overwrite)

    for filename, factory in factories:
        if factory(os.path.join(path, filename), overwrite=filename in overwrite):
            extraignore.append("/" + filename)


def get_singularity_root(binary_tag: str):
    """
    >>> get_singularity_root("x86_64-centos7-gcc9-opt")
    '/cvmfs/cernvm-prod.cern.ch/cvm4'
    >>> get_singularity_root("x86_64-slc6-gcc9-opt")
    '/cvmfs/cernvm-prod.cern.ch/cvm3'
    >>> get_singularity_root("x86_64-slc5-gcc9-opt")
    '/cvmfs/cernvm-prod.cern.ch/cvm3'
    >>> get_singularity_root("x86_64-ubuntu-gcc9-opt")
    >>>
    """
    from LbPlatformUtils import OS_ALIASES, OS_COMPATIBILITY
    from LbPlatformUtils.inspect import SINGULARITY_ROOTS

    wanted_os = binary_tag.split("-")[1]
    compatible_oss = [wanted_os] + [
        main_os
        for main_os, comp_oss in OS_COMPATIBILITY.items()
        if wanted_os in comp_oss
    ]
    try:
        compatible_aliases = [
            comp_os
            for compatible_os in compatible_oss
            for comp_os in OS_ALIASES[compatible_os]
        ]
        return [path for path, osid in SINGULARITY_ROOTS if osid in compatible_aliases][
            0
        ]
    except (IndexError, KeyError):
        return None


def to_cmake_version(v):
    """
    Helper to convert "vXrYpZ" to "X.Y.Z".

    >>> to_cmake_version('v1r0p0')
    '1.0.0'
    """
    return ".".join(re.findall(r"\d+", v))


def build_env(project, platform):
    """
    Set environment for building the nightlies.
    """
    build_env = {}
    build_env["BINARY_TAG"] = build_env["CMTCONFIG"] = platform
    path_items = [
        f"{os.environ['PATH']}",
        "/cvmfs/lhcb.cern.ch/lib/bin/x86_64-centos7",
        "/cvmfs/lhcb.cern.ch/lib/bin/Linux-x86_64",
        "/cvmfs/lhcb.cern.ch/lib/bin",
    ]
    build_env["PATH"] = ":".join(path_items)
    build_env["LBENV_CURRENT_WORKSPACE"] = str(project.slot.get_deployment_directory())
    cmake_prefix_path_items = [
        build_env["LBENV_CURRENT_WORKSPACE"],
        "/cvmfs/lhcb.cern.ch/lib/lhcb",
        "/cvmfs/lhcb.cern.ch/lib/lcg/releases",
        "/cvmfs/lhcb.cern.ch/lib/contrib",
        CMAKE_DIR,
        "/cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/vtune_amplifier",
    ]
    build_env["CMAKE_PREFIX_PATH"] = ":".join(cmake_prefix_path_items)
    if "TASK_LOGFILE" in os.environ:
        build_env["TASK_LOGFILE"] = os.environ["TASK_LOGFILE"]
    if "CONDA_ENV" in os.environ:
        build_env["CONDA_ENV"] = os.environ["CONDA_ENV"]
    build_env["SINGULARITY_ROOT"] = get_singularity_root(platform)
    build_env["NIGHTLIES_CACHE"] = lbnightly_settings().installations.path
    build_env["slot"] = project.slot.name
    build_env["slot_build_id"] = str(project.slot.build_id)

    return build_env


def compute_env(project, init_env=None, override_env=None):
    """
    Compute the environment for the project.
    """
    new_env = project.environment(envdict=init_env)
    if override_env:
        new_env.update(override_env)
    # make sure that slot deployment directory is the first one in CMAKE_PREFIX_PATH
    if project.slot:
        cmake_paths = new_env.get("CMAKE_PREFIX_PATH", "").split(":")
        deployment_dir = str(project.slot.get_deployment_directory())
        if cmake_paths[0] != deployment_dir:
            new_env["CMAKE_PREFIX_PATH"] = ":".join(
                [deployment_dir]
                + [item for item in cmake_paths if item != deployment_dir]
            )

    return new_env


def deployment_ready(path: Path, stage: str, platform: str = None) -> bool:
    """
    Helper to check if a deployment of nightly artifact is available.
    """
    if stage == "checkout":
        return path.exists() and any(
            item
            for item in path.iterdir()
            if item.name not in {"InstallArea", ".cvmfscatalog"}
        )
    elif stage == "build":
        build_path = path / "InstallArea" / platform
        return build_path.exists() and any(build_path.iterdir())
    return False


def deployments_ready(project: Project, platform: str, stage: str) -> bool:
    """
    Function to check if all the deployments needed to run a nightly task are available
    """
    if stage in {"build", "test"}:
        if not deployment_ready(project.get_deployment_directory(), "checkout"):
            return False
        if stage == "test":
            if not deployment_ready(
                project.get_deployment_directory(), "build", platform
            ):
                return False
        for dep_name in project.dependencies():
            if dep_name in project.slot.projects:
                dependency = project.slot.projects[dep_name]
                if dependency.enabled:
                    if isinstance(dependency, (Package, DataProject)):
                        if not deployment_ready(
                            dependency.get_deployment_directory(), "checkout"
                        ):
                            return False
                    elif isinstance(dependency, Project):
                        if not deployment_ready(
                            dependency.get_deployment_directory(), "build", platform
                        ):
                            return False
    return True


def wait_for_deployment_dirs(
    project: Project,
    platform: str,
    stage: str = "build",
):
    """
    Helper to wait for all the deployments needed to build or test given project.
    Raises RuntimError if max time is exceeded.
    """
    start = datetime.now()
    while datetime.now() - start < MAX_TIME_WAITING_FOR_DEPLOYMENT:
        if deployments_ready(project, platform, stage):
            return
        sleep(TIME_BETWEEN_DEPLOYMENT_CHECKS.total_seconds())
    raise RuntimeError(
        f"Giving up after waiting for deployment "
        f"directories needed to run {stage} of "
        f"{project} {platform}"
    )
