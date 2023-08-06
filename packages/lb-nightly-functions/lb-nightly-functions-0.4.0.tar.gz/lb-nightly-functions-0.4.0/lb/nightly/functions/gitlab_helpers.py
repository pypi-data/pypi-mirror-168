###############################################################################
# (c) Copyright 2020-2021 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import logging
import os
from datetime import datetime
from typing import Union

import gitlab
from lb.nightly.configuration import Package, Project


def get_gitlab_url(project: Union[Project, Package]):
    """
    Deduce the Gitlab Git URL for the given project.
    """
    # FIXME: the default URL should be retrieved from SoftConfDb
    if not isinstance(project, Package):
        group = "gaudi" if project.name == "Gaudi" else "lhcb"
    else:
        group = "lhcb-datapkg"
    return project.checkout_opts.get(
        "url", f"https://gitlab.cern.ch/{group}/{project.name}.git"
    )


def get_gitlab_id(url):
    """
    Deduce the Gitlab id for the given project URL.
    """
    from urllib.parse import urlparse

    gitlab_id = urlparse(url).path.lstrip("/")
    if gitlab_id.endswith(".git"):
        gitlab_id = gitlab_id[:-4]

    return gitlab_id


def postToMergeRequest(
    name_or_id, mreq_iid, message, new_comment=False, token=None, logger=logging
):
    """
    Add the passed message as comment to a merge request in gitlab.cern.ch.

    @param name_or_id: qualified name or id of a project in gitlab
    @param mreq_iid: local id of the merge request
    @param message: what to post to the merge request
    @param new_comment: whether to always post a new comment or edit
    @param token: gitlab API token (default: os.environ['GITLAB_TOKEN'])
    """
    server = gitlab.Gitlab(
        "https://gitlab.cern.ch/", token or os.environ["GITLAB_TOKEN"]
    )
    logger.debug("looking for merge request %s in project %s", mreq_iid, name_or_id)
    try:
        project = server.projects.get(name_or_id)
        mreq = project.mergerequests.get(mreq_iid)
        if new_comment:
            mreq.notes.create({"body": message})
        else:
            time_tag = datetime.now().strftime("%Y-%m-%d %H:%M")
            message = "- __[{}]__ {}".format(time_tag, message)
            server.auth()  # sets server.user to the authenticated user
            all_notes = mreq.notes.list(order_by="created_at", sort="desc")
            # NB: replying to a plain note makes it a discussion, so next
            # time it won't be found and a new one will be made.
            own_plain_notes = [
                note
                for note in all_notes
                if (
                    note.author["id"] == server.user.id
                    and not note.system
                    and note.type != "DiscussionNote"
                )
            ]
            if own_plain_notes:
                last_note = own_plain_notes[0]
                last_note.body = last_note.body + "\n" + message
                last_note.save()
            else:
                mreq.notes.create({"body": message})
    except Exception as err:
        logger.error(str(err))
        raise


def getMRTitle(name_or_id, mreq_iid, token=None, logger=logging):
    """
    Return the title of a merge request in gitlab.cern.ch.

    @param name_or_id: qualified name or id of a project in gitlab
    @param mreq_iid: local id of the merge request
    @param token: gitlab API token (default: os.environ['GITLAB_TOKEN'])
    """
    token = token or os.environ.get("GITLAB_TOKEN")
    if not token:
        # the MR title is icing on the cake, we do not need to fail
        return ""

    server = gitlab.Gitlab("https://gitlab.cern.ch/", token)
    logger.debug("looking for merge request %s in project %s", mreq_iid, name_or_id)
    try:
        project = server.projects.get(name_or_id)
        mreq = project.mergerequests.get(mreq_iid)
        return mreq.title
    except Exception as err:
        logger.error(str(err))
        raise


def gitlabProjectExists(project, logger=logging):
    """
    Quick check to see if a project exists and is public in Gitlab.
    """
    from urllib.request import urlopen

    try:
        logger.debug("probing %s in Gitlab", project)
        url = (
            "https://gitlab.cern.ch/{}.git/info/refs?service=git-upload-pack"
        ).format(project)
        return urlopen(url).getcode() == 200
    except Exception:
        return False


MR_COMMENT_TMPLS = {
    True: (
        "Validation started with [{slot}#{id}]("
        "https://lhcb-nightlies.web.cern.ch/nightly/{slot}/{id}/)"
    ),
    False: (
        "Automatic merge failed in [{slot}#{id}]("
        "https://lhcb-nightlies.web.cern.ch/nightly/{slot}/{id}/{proj}/checkout"
    ),
}


def notifyMergeRequest(
    proj: Project, name_or_id, mreq_iid, success, token=None, logger=logging
):
    """
    Post the link to the slot build as comment to a merge request.
    """
    if (
        not proj
        or not proj.slot
        or not proj.slot.build_id
        or (os.environ.get("NO_UPDATE_MR", "false").lower() not in ("false", "0", ""))
    ):
        # noting to notify
        return
    if not token and "GITLAB_TOKEN" not in os.environ:
        logger.warning(
            "cannot post comment to gitlab for project %s, mr %s", name_or_id, mreq_iid
        )
        return

    message = MR_COMMENT_TMPLS[success].format(
        slot=proj.slot.name, id=proj.slot.build_id, proj=proj.name
    )
    postToMergeRequest(name_or_id, mreq_iid, message, token=token)
