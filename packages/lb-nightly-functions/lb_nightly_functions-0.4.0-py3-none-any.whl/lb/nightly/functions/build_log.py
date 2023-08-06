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
import html
import os
import re

MAX_REPORTED_ISSUES = 100  # per severity
_ESCAPE_SEQ = re.compile("\x1b\\[([0-9;]*m|[012]?K)")


def remove_colors(text):
    """
    Strip ANSI color codes from a text.

    >>> remove_colors('\\x1b[34;42mHello\\x1b[2m!\\x1b[m')
    'Hello!'
    """
    return _ESCAPE_SEQ.sub("", text)


_LOG_SCANNERS = []


def log_scanner(func):
    """
    Decorator to declare a function as log scanner.
    """
    global _LOG_SCANNERS
    _LOG_SCANNERS.append(func)
    return func


class IssueSource(object):
    def __init__(self, name, line=None, pos=None):
        self.name = name
        self.line = line
        self.pos = pos

    def __str__(self):
        return ":".join(str(s) for s in [self.name, self.line, self.pos] if s)

    def __repr__(self):
        return "IssueSource{0!r}".format(
            tuple(s for s in [self.name, self.line, self.pos] if s)
        )


class Issue:
    """
    Base class for issues found in logs.
    """

    SEVERITIES = ("error", "warning", "coverity")

    def __init__(self, severity, source, msg, log_range):
        if severity not in self.SEVERITIES:
            raise ValueError("invalid severity value %r", severity)
        self.severity = severity
        if isinstance(source, tuple):
            source = IssueSource(*source)
        self.source = source
        self.msg = msg
        self.log_range = log_range

    def linkText(self):
        return "{}:{}".format(self.source.name, self.source.line)

    def __str__(self):
        return ": ".join(str(s) for s in [self.source, self.severity, self.msg])

    def __repr__(self):
        return "{0}{1!r}".format(
            self.__class__.__name__,
            (self.severity, self.source, self.msg, self.log_range),
        )


class IssueLinker:
    def __init__(self, issues, url_format):
        self.issues = issues
        self.url_format = url_format
        self._count = 0

    def __call__(self, line):
        n = self._count
        for issue in self.issues:
            l, h = issue.log_range
            if n >= l and n < h:
                txt = html.escape(issue.linkText(), quote=True)
                line = line.replace(
                    txt,
                    '<a href="{url}">{txt}</a>'.format(
                        url=self.url_format(issue.source), txt=txt
                    ),
                )
                break
        self._count += 1
        return line


class GitlabUrlFormat:
    def __init__(self, base_url):
        base_url = base_url.rstrip("/")
        self.format = base_url + "/{name}#L{line}"

    def __call__(self, source):
        return self.format.format(name=source.name, line=source.line)


def reports2exclusions(reports=None):
    """
    Translate a list of Issue instances to a list of lines to exclude in an
    enumeration.

    >>> reports2exclusions([Issue('warning', ('f1',), 'm1', (10, 15)),
    ...                     Issue('warning', ('f2',), 'm2', (23, 27)),
    ...                     Issue('error', ('f3',), 'm3', (18, 19))])
    [(10, 15), (18, 19), (23, 27)]
    """
    if not reports:
        return None
    exclusions = [issue.log_range for issue in reports]
    exclusions.sort()
    return exclusions


def enumerate_x(items, exclusions=None):
    """
    Same as builtin enumerate function, but skip items with id in the ranges
    defined by exclusions.

    >>> list(enumerate_x('abcdefghij', [(2, 5), (8, 9)]))
    [(0, 'a'), (1, 'b'), (5, 'f'), (6, 'g'), (7, 'h'), (9, 'j')]

    Exclusions may be overlapping:

    >>> list(enumerate_x('abcdefghij', [(1, 4), (2, 5), (6, 9), (7, 8)]))
    [(0, 'a'), (5, 'f'), (9, 'j')]
    """
    if not exclusions:
        return enumerate(items)
    from itertools import chain

    # invert the exclusions to list of partial enumerations
    ranges = []
    start = 0
    for stop, next_start in exclusions:
        # if there is an overlap in the exclusion we need to skip to the next
        if stop >= start:
            ranges.append(enumerate(items[start:stop], start))
        # max here covers the case of full enclosed exclusions ([(2,10), (3,5)])
        start = max(start, next_start)
    ranges.append(enumerate(items[start:], start))
    # return the joined partial enumerations
    return chain(*ranges)


class GCCIssue(Issue):
    pass


@log_scanner
def gcc_output_scanner(lines, reports=None):
    if reports is None:
        reports = []
    diag_rexp = re.compile(r"^(\S+):([0-9]+):([0-9]+): (warning|error): (.*)")
    try:
        ln_iter = enumerate_x(lines, reports2exclusions(reports))
        ln, line = next(ln_iter)
        while True:
            line = remove_colors(line.rstrip())
            m = diag_rexp.match(line)
            if m:
                startln = ln
                ln, line = next(ln_iter)
                try:
                    while line.startswith(" "):
                        ln, line = next(ln_iter)
                except StopIteration:
                    pass
                reports.append(
                    GCCIssue(
                        m.group(4),
                        (m.group(1), int(m.group(2)), int(m.group(3))),
                        m.group(5),
                        (startln, ln),
                    )
                )
            else:
                ln, line = next(ln_iter)
    except StopIteration:
        pass
    return reports


class CMakeIssue(Issue):
    pass


@log_scanner
def cmake_output_scanner(lines, reports=None):
    if reports is None:
        reports = []
    diag_rexp = re.compile(
        r"^CMake (?:Deprecation )?(Warning|Error) (?:\(dev\) )?at (\S+):([0-9]+) \(message\):"
    )
    try:
        ln_iter = enumerate_x(lines, reports2exclusions(reports))
        ln, line = next(ln_iter)
        while True:
            line = line.rstrip()
            m = diag_rexp.match(line)
            if m:
                startln = ln
                ln, line = next(ln_iter)
                try:
                    while line.startswith(" "):
                        ln, line = next(ln_iter)
                except StopIteration:
                    pass
                msg = " ".join(l.strip() for l in lines[startln + 1 : ln]).strip()
                if len(msg) > 120:
                    msg = msg[:80] + "[...]" + msg[-35:]
                reports.append(
                    CMakeIssue(
                        m.group(1).lower(),
                        (m.group(2), int(m.group(3))),
                        msg,
                        (startln, ln),
                    )
                )
            else:
                ln, line = next(ln_iter)
    except StopIteration:
        pass
    return reports


class GaudiIssue(Issue):
    pass


@log_scanner
def gaudi_output_scanner(lines, reports=None):
    if reports is None:
        reports = []
    diag_rexp = re.compile(r".*?(\S+) *(WARNING|ERROR|FATAL) +(.*)")
    try:
        ln_iter = enumerate_x(lines, reports2exclusions(reports))
        ln, line = next(ln_iter)
        while True:
            line = line.rstrip()
            m = diag_rexp.match(line)
            if m:
                diag_type = m.group(2).lower()
                if diag_type == "fatal":
                    diag_type = "error"
                reports.append(
                    GaudiIssue(diag_type, (m.group(1),), m.group(3), (ln, ln + 1))
                )
            ln, line = next(ln_iter)
    except StopIteration:
        pass
    return reports


class PythonIssue(Issue):
    def linkText(self):
        return 'File "{}", line {}'.format(self.source.name, self.source.line)


@log_scanner
def python_output_scanner(lines, reports=None):
    if reports is None:
        reports = []
    warn_rexp = re.compile(r"(\S+):([0-9]+): \S*(Warning): (.*)")
    tbinfo_rexp = re.compile(r'\s+File "(.+)", line ([0-9]+)')
    try:
        ln_iter = enumerate_x(lines, reports2exclusions(reports))
        ln, line = next(ln_iter)
        while True:
            line = line.rstrip()
            m = warn_rexp.match(line)
            if m:
                startln = ln
                ln, line = next(ln_iter)
                reports.append(
                    PythonIssue(
                        "warning",
                        (m.group(1), int(m.group(2))),
                        m.group(4),
                        (startln, ln),
                    )
                )
            elif line.strip() == "Traceback (most recent call last):":
                startln = ln
                ln, line = next(ln_iter)
                filename, fileln, msg = "<unkown>", None, "Python traceback"
                try:
                    while line.startswith(" "):
                        ln, line = next(ln_iter)
                        m = tbinfo_rexp.match(line)
                        if m:
                            filename = m.group(1)
                            fileln = int(m.group(2))
                    # the actual exception message is after of the dump
                    msg = line.strip()
                    ln, line = next(ln_iter)
                except StopIteration:
                    pass
                reports.append(
                    PythonIssue("error", (filename, fileln), msg, (startln, ln))
                )
            else:
                ln, line = next(ln_iter)
    except StopIteration:
        pass
    return reports


class ROOTBreakIssue(Issue):
    pass


@log_scanner
def root_stack_trace_output_scanner(lines, reports=None):
    if reports is None:
        reports = []
    MARKER = "*** Break ***"
    try:
        ln_iter = enumerate_x(lines, reports2exclusions(reports))
        ln, line = next(ln_iter)
        while True:
            line = line.strip()
            if line.startswith(MARKER):
                msg = line[len(MARKER) :].strip()
                reports.append(
                    ROOTBreakIssue("error", ("<unknown>",), msg, (ln, ln + 1))
                )
            ln, line = next(ln_iter)
    except StopIteration:
        pass
    return reports


class GenericIssue(Issue):
    def __str__(self):
        return self.msg


@log_scanner
def generic_scanner(lines, reports=None):
    if reports is None:
        reports = []
    WARNING_RE = re.compile(
        "|".join([r"\bwarning\b", r"\bSyntaxWarning:"]), re.IGNORECASE
    )
    ERROR_RE = re.compile(
        "|".join(
            [
                r"\berror\b",
                r"\*\*\* Break \*\*\*",
                r"^Traceback \(most recent call last\):",
                r"^make: \*\*\* No rule to make target",
                r"Assertion.*failed",
            ]
        ),
        re.IGNORECASE,
    )
    try:
        ln_iter = enumerate_x(lines, reports2exclusions(reports))
        ln, line = next(ln_iter)
        while True:
            line = remove_colors(line.strip())
            diag_type = (WARNING_RE.search(line) and "warning") or (
                ERROR_RE.search(line) and "error"
            )
            if diag_type:
                reports.append(
                    GenericIssue(diag_type, ("<unknown>",), line, (ln, ln + 1))
                )
            ln, line = next(ln_iter)
    except StopIteration:
        pass
    return reports


def scan_build_log(lines):
    reports = None
    if isinstance(lines, str):
        lines = lines.splitlines()
    for scanner in _LOG_SCANNERS:
        reports = scanner(lines, reports)
    return reports


def report_dict(chunks, reports):
    """
    Convert list of (chunk_id, lines) and a dictionary {chunk_id: issues} into
    a simplified report suitable for conversion to JSON.

    The output format is:

        {'sections': [{'id': 'section_id',
                       'desc': 'html title of the section',
                       'url': 'url of section content (html)'}, ...],
         'issues': {
             'severity': [{
                  'section_id': 'id of section it comes from',
                  'anchor': 'html anchor in section content',
                  'desc': 'one line description of the issue',
                  'text': ['full issue', 'report', ...]
             }, ...],
             ...
        }}
    """
    report = {"sections": [], "issues": {severity: [] for severity in Issue.SEVERITIES}}

    for chunk_id, chunk in chunks:
        report["sections"].append(
            {"id": chunk_id, "desc": chunk_id, "url": "{}.html".format(chunk_id)}
        )
        for issue in reports[chunk_id]:
            report["issues"][issue.severity].append(
                {
                    "section_id": chunk_id,
                    "anchor": "{0}_{1}".format(chunk_id, issue.log_range[0] + 1),
                    "desc": html.escape(str(issue), quote=True),
                    "text": [
                        html.escape(remove_colors(line.rstrip()), quote=True)
                        for line in chunk[issue.log_range[0] : issue.log_range[1]]
                    ],
                }
            )
    return report


TABLE_HEAD = '<table class="table table-striped" style="text-align:left">'
TABLE_TAIL = "</table>"


def generate_build_report(
    build_logs={},
    proj_build_root=None,
    exceptions=None,
    extra_info=None,
):
    from os.path import isdir, join
    from subprocess import CalledProcessError, check_output

    # collect git infos
    git_info = {}
    try:
        if proj_build_root and isdir(join(proj_build_root, ".git")):
            # we can only support projects with checkout recorded in
            # https://gitlab.cern.ch/lhcb-nightlies
            url = check_output(
                ["git", "config", "remote.lhcb-nightlies.url"], cwd=proj_build_root
            )
            git_info["name"] = os.path.basename(os.path.splitext(url)[0])

            git_info["commit"] = check_output(
                ["git", "rev-parse", "HEAD"], cwd=proj_build_root
            ).strip()
            git_info["files"] = set(
                check_output(
                    ["git", "ls-tree", "--name-only", "-r", "HEAD"], cwd=proj_build_root
                ).splitlines()
            )
            git_info["url"] = (
                "https://gitlab.cern.ch/lhcb-nightlies/" "{name}/blob/{commit}/"
            ).format(**git_info)
    except CalledProcessError:
        # could not extract git info
        git_info = {}

    reports = {}
    legacy_build_logs = []

    for subdir, logs in build_logs.items():
        data = []
        for target_name, target_actions in logs.items():
            for action_result in target_actions:
                data.append(" ".join(action_result["cmd"]))
                if action_result["stdout"]:
                    data.append(action_result["stdout"])
                if action_result["stderr"]:
                    data.append(action_result["stderr"])
                # scan_build_log uses the line numbers in the chunk of data
                # it is given, but the report links point to the full stderr block
                action_issues = scan_build_log(action_result["stderr"])
                for issue in action_issues:
                    # set (artificially) the line number range to the
                    # current stderr block in the subdir (later used to
                    # create HTML anchors)
                    issue.log_range = (len(data) - 1, len(data))
                reports.setdefault(subdir, []).extend(action_issues)
        legacy_build_logs.append((subdir, data))

    from .html_utils import ANSI2HTML, ClassifyByLineNo, TableizeLine, WrapLine

    html_section = {}
    for chunk_id, chunk in legacy_build_logs:
        classification = ClassifyByLineNo(
            (
                (issue.log_range[0] + 1, issue.log_range[1] + 1),
                {"warning": "alert-warning", "error": "alert-danger"}.get(
                    issue.severity, ""
                ),
            )
            for issue in reports[chunk_id]
        )
        actions = [
            lambda line: html.escape(line, quote=True),
            ANSI2HTML(),
            WrapLine("pre"),
            TableizeLine(
                line_id_prefix=chunk_id + "_",
                add_line_nos=True,
                row_class=classification,
            ),
        ]
        if git_info:
            actions.append(
                IssueLinker(
                    [
                        issue
                        for issue in reports[chunk_id]
                        if issue.source.name in git_info["files"]
                    ],
                    GitlabUrlFormat(git_info["url"]),
                )
            )

        def process(line):
            for action in actions:
                line = action(line)
            return line

        html_section[chunk_id] = TABLE_HEAD
        for line in (process(line.rstrip()) + "\n" for line in chunk):
            html_section[chunk_id] += line + "\n"
        html_section[chunk_id] += TABLE_TAIL

    jreport = report_dict(legacy_build_logs, reports)
    jreport["raw_logs"] = build_logs
    for section in jreport["sections"]:
        section["html"] = html_section[section["id"]]

    # filter issues to remove excluded ones
    jreport["ignored_issues"] = {severity: {} for severity in jreport["issues"]}
    exceptions = {
        severity: [(exp, re.compile(exp)) for exp in exceptions[severity]]
        for severity in exceptions or {}
    }
    for severity in exceptions:
        # remove excluded issues from the report and count them per regexp
        for text, exp in exceptions[severity]:
            before = len(jreport["issues"][severity])
            jreport["issues"][severity] = [
                issue
                for issue in jreport["issues"][severity]
                if not exp.search(issue["desc"])
            ]
            after = len(jreport["issues"][severity])
            jreport["ignored_issues"][severity][text] = before - after

    jreport.update(
        {
            "warnings": len(jreport["issues"]["warning"]),
            "errors": len(jreport["issues"]["error"]),
            "coverity_messages": len(jreport["issues"]["coverity"]),
        }
    )

    # limit the number of presented issues (see LBCORE-1210)
    # it's done here because I want jreport[severity's] to contain the total
    for severity in jreport["issues"]:
        count = len(jreport["issues"][severity])
        if count > MAX_REPORTED_ISSUES:
            jreport["ignored_issues"][severity]["too many issues"] = (
                count - MAX_REPORTED_ISSUES
            )
            jreport["issues"][severity][MAX_REPORTED_ISSUES:] = []

    # group repeated warnings
    issues = {"errors": {}, "warnings": {}, "coverity": {}}
    for (key, issue_type) in [
        ("errors", "error"),
        ("warnings", "warning"),
        ("coverity", "coverity"),
    ]:
        for issue in jreport["issues"][issue_type]:
            issues[key].setdefault(issue["desc"], {}).setdefault(
                issue["section_id"], []
            ).append(issue["anchor"])
    jreport["issues"] = {
        key: [{"desc": desc, "where": where} for desc, where in issues[key].items()]
        for key in issues
    }

    if extra_info:
        jreport.update(extra_info)

    return jreport
