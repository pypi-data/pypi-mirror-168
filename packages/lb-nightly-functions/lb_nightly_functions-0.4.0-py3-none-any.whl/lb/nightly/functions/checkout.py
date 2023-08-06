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
import os
import re
from typing import Union

from git import Git, GitCommandError, Repo
from lb.nightly.configuration import DataProject, Package, Project

from .common import Report
from .gitlab_helpers import get_gitlab_id, get_gitlab_url


def git(project: Union[Project, Package]):
    """
    Checkout a project in the current directory.

    project has to be a Project instance from lb.nightly.configuration

    Return logging data in the form of a list of messages and executed commands.
    """
    if not isinstance(project, (Project, Package)):
        raise TypeError(
            f"expected lb.nightly.configuration.Project instance, not {type(project).__name__}"
        )

    rep = Report(f"{__name__}.git")
    rep.project = {
        "name": project.name,
        "version": project.version,
        "options": project.checkout_opts,
    }
    rep.merges = {"success": [], "failure": []}
    rep.submodules = {"success": [], "failure": []}
    rep.commit = None
    rep.tree = None

    if isinstance(project, DataProject):
        # Data projects must be handled in a special way
        rep.packages = [git(pack) for pack in project.packages]
        return rep

    url = get_gitlab_url(project)
    rep.gitlab_id = get_gitlab_id(url)
    if hasattr(project, "container") and project.container:
        path = os.path.join(
            os.getcwd(), project.container.name, project.name, project.version
        )
    else:
        path = os.path.join(os.getcwd(), project.name)

    def submodule_recursion(submodules, path=path):
        """
        Call "git update" on the passed list of submodules
        and all their children.
        """
        for s in submodules:
            target_path = os.path.join(path, s.path)
            rep.info(f"updating submodule {s.name} in {target_path}")
            try:
                s.update()
                rep.submodules["success"].append(s.name)
                submodule_recursion(s.children(), target_path)
            except GitCommandError as err:
                rep.submodules["failure"].append(s.name)
                rep.git_error(f"{s.name}: warning: failed to get submodule", err)

    rep.info(f"cloning {url} into {path}")

    if not os.path.exists(path):
        repo = Repo.clone_from(url, path, no_checkout=True)
    else:
        repo = Repo(path)

    # pick up requested commit
    if "commit" in project.checkout_opts:
        repo.head.reference = repo.commit(project.checkout_opts["commit"])
    elif project.version.lower() == "head":
        pass  # trust default commit
    elif project.version in repo.remotes.origin.refs:  # check if version is a branch
        repo.head.reference = repo.remotes.origin.refs[project.version]
    elif project.version in repo.refs:  # check if version is a tag
        repo.head.reference = repo.refs[project.version]
    else:
        raise ValueError(f"no 'commit' option and invalid version for {project}")
    rep.info(f"using commit {repo.head.commit.hexsha} for {project.version}")

    repo.head.reset(index=True, working_tree=True)
    git_cmd = Git(repo.working_dir)

    for mr_iid, commit_id in project.checkout_opts.get("merges", []):
        try:
            rep.info(f"merging {rep.gitlab_id}!{mr_iid} ({commit_id})")
            fetches = repo.remote("origin").fetch(commit_id)
            commit = fetches[0].commit
            rep.log(
                "stdout",
                "debug",
                git_cmd.merge(
                    commit, no_ff=True, message=f"merged {rep.gitlab_id}!{mr_iid}"
                ),
            )
            rep.merges["success"].append(mr_iid)
        except GitCommandError as err:
            rep.git_error(
                f"warning: failed to merge {rep.gitlab_id}!{mr_iid} ({commit_id})", err
            )
            rep.info("reverting to previous state")
            repo.head.reset(index=True, working_tree=True)
            rep.merges["failure"].append(mr_iid)

    submodule_recursion(repo.submodules)

    if hasattr(project, "container"):
        # for data packages we have to detect the internal version and
        # create the appropriate symlinks
        # - we always need a v999r999 link
        os.symlink(
            os.path.basename(path), os.path.join(os.path.dirname(path), "v999r999")
        )
        # - find the major version number
        try:
            with open(os.path.join(path, "cmt", "requirements")) as req:
                for l in req:
                    m = re.match(r"\s*version\s+v(\d+)r", l)
                    if m:
                        # we found the magic line, so we can create the link
                        os.symlink(
                            os.path.basename(path),
                            os.path.join(
                                os.path.dirname(path), "v{}r999".format(m.group(1))
                            ),
                        )
                        break
        except IOError:
            pass  # we do not really care if there's no cmt/requirements or is unreadable

    rep.commit = repo.head.commit.hexsha
    rep.tree = repo.head.commit.tree.hexsha
    rep.info("result:\n  commit: %s\n  tree: %s", rep.commit, rep.tree)

    return rep


def notify_gitlab(project: Union[Project, Package], report: Report, token: str = None):
    """
    Update merge requests discussions with links to the slot the project
    was built in, specifying if the merge was successful or not.

    The ``report`` argument should be the return value of a call to
    the ``git`` function.
    """
    from .gitlab_helpers import notifyMergeRequest

    if not hasattr(report, "gitlab_id"):
        report.gitlab_id = get_gitlab_id(get_gitlab_url(project))

    report.debug("notifying gitlab project %s", report.gitlab_id)
    try:
        for mr_iid in report.merges.get("success", []):
            notifyMergeRequest(project, report.gitlab_id, mr_iid, True, token, report)
        for mr_iid in report.merges.get("failure", []):
            notifyMergeRequest(project, report.gitlab_id, mr_iid, False, token, report)
    except AttributeError:
        report.warning("summary of merge results missing in report")

    return report


def update_nightly_git_archive(project: Union[Project, Package], report: Report):
    """
    Record the archives of the nightly builds in
    https://gitlab.cern.ch/lhcb-nightlies

    A new tags from slot name and build id is created, and the slot
    branch is updated, if needed.

    The ``report`` argument should be the return value of a call to
    the ``git`` function.
    """
    from .gitlab_helpers import gitlabProjectExists

    assert (
        project.slot and project.slot.build_id
    ), "Only projects in built slots can be recorded in https://gitlab.cern.ch/lhcb-nightlies"

    if not gitlabProjectExists(f"lhcb-nightlies/{project.name}"):
        report.warning(
            f"{project.name} not found on https://gitlab.cern.ch/lhcb-nightlies, not recording build sources"
        )
        return report

    report.info(
        f"recording checkout state in https://gitlab.cern.ch/lhcb-nightlies/{project.name}"
    )
    repo = Repo(project.name)
    nightlies = repo.create_remote(
        "nightlies", f"ssh://git@gitlab.cern.ch:7999/lhcb-nightlies/{project.name}.git"
    )

    # fetch guessed "previous" tag (build_id - 1)
    try:
        previous_tag = repo.create_tag(
            f"{project.slot.name}/{project.slot.build_id - 1}",
            nightlies.fetch(f"{project.slot.name}/{project.slot.build_id - 1}")[
                0
            ].commit,
        )
    except GitCommandError:
        previous_tag = None

    # fetch the slot specific branch from the archive
    try:
        tracking_branch = repo.create_head(
            project.slot.name, nightlies.fetch(project.slot.name)[0].commit
        )
    except GitCommandError:
        report.debug(
            f"failed to fetch branch {project.slot.name} from {nightlies.url}, trying to create it"
        )
        if previous_tag:
            tracking_branch = repo.create_head(project.slot.name, previous_tag.commit)
        else:
            tracking_branch = repo.create_head(project.slot.name, repo.head.commit)

    if previous_tag and previous_tag.commit.tree.hexsha == report.tree:
        # same content of previous tag, just re-use that commit
        repo.head.reset(previous_tag.commit)
    elif tracking_branch.commit.tree.hexsha == report.tree:
        # same content as tip of reference branch, re-use that commit
        repo.head.reset(tracking_branch.commit)
    else:
        # no commit to re-use, create a new merge commit on top of the
        repo.index.commit(
            f"changes for {project.slot.name}/{project.slot.build_id}",
            parent_commits=(tracking_branch.commit, repo.head.commit),
        )
        tracking_branch.commit = repo.head.commit
    # create the new tag
    new_tag = repo.create_tag(f"{project.slot.name}/{project.slot.build_id}")

    assert (
        report.tree == repo.head.commit.tree.hexsha
    ), "tree content mismatch after nightlies archive update"

    nightlies.push([tracking_branch, new_tag])

    # log changes, if any
    if previous_tag and previous_tag.commit.tree.hexsha != report.tree:
        report.info(f"changes detected wrt {previous_tag.name}")
        report.log(
            "command",
            "debug",
            f"git show-branch --sha1-name {previous_tag.name} {new_tag.name}",
        )
        report.log(
            "stdout",
            "debug",
            repo.git.show_branch([previous_tag, new_tag], sha1_name=True, color=True),
        )
        report.log(
            "command",
            "debug",
            f"git diff --stat {previous_tag.name} {new_tag.name}",
        )
        # find a reasonable report width to avoid truncation of names
        # - use the biggest between 120 and the max size of names + 20
        width = max(
            120,
            max(
                len(l)
                for l in repo.git.diff(
                    [previous_tag, new_tag], z=True, name_only=True
                ).split("\0")
            )
            + 20,
        )
        report.log(
            "stdout",
            "debug",
            repo.git.diff(
                [previous_tag, new_tag],
                stat=f"{max(width + 20, 120)}",
                color=True,
            ),
        )
    elif previous_tag:
        report.info(f"no change wrt {previous_tag.name}")
    else:
        report.info(f"no previous tag found, comparison not available")

    # update the commit id in the report (the tree did not change by
    # construction)
    report.commit = repo.head.commit.hexsha

    return report
