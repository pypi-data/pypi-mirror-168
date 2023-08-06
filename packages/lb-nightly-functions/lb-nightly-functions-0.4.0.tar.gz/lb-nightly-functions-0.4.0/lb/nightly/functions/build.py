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
from datetime import datetime
from pathlib import Path
from shlex import quote

from lb.nightly.configuration import Project

from .common import (
    Report,
    compute_env,
    ensure_dir,
    find_path,
    init_project,
    singularity_run,
    to_cmake_version,
)


class cmake_new:

    # known "kwargs" not to be propagated to subprocess
    SPECIAL_ARGS = (
        "jobs",
        "args",
        "make_cmd",
        "cache_entries",
        "step",
        "relaxed_install",
    )

    def __init__(self, project: Project) -> None:
        self.project = project
        if not isinstance(self.project, Project):
            raise TypeError(
                f"expected lb.nightly.configuration.Project instance, "
                f"not {type(project).__name__}"
            )
        self.reports = {}
        for step in [
            "configure",
            "build",
            "install",
            "clean",
            "test",
            "script",
        ]:
            self.reports[step] = Report(f"{__name__}_{step}.cmake_new")
        self.build_logs = {}

    @property
    def build_dir(self):
        return Path(self.project.name) / "build"

    def _cache_preload_file(self) -> Path:
        """
        Name of the cache preload file to be passed to CMake.
        """
        return self.build_dir / "cache_preload.cmake"

    def _prepare_cache(
        self,
        cache_entries=None,
    ):
        """
        Prepare the cache_preload.cmake file passed to CMake during the
        configuration.
        """
        # prepare the cache to give to CMake: add the launcher rules commands,
        # followed by what is found passed as argument
        if cache_entries is None:
            cache_entries = []
        elif hasattr(cache_entries, "items"):
            cache_entries = list(cache_entries.items())

        cache_file = self._cache_preload_file()
        ensure_dir(os.path.dirname(cache_file), self.reports["configure"])
        with open(cache_file, "w") as cache:
            cache.writelines(
                [
                    'set(%s "%s" CACHE STRING "override")\n' % item
                    for item in cache_entries
                ]
            )
            # force use of ccache
            cache.writelines(
                'set(CMAKE_{}_COMPILER_LAUNCHER ccache CACHE STRING "override")\n'.format(
                    lang
                )
                for lang in ("C", "CXX")
            )
            # enable rule wrappers
            cache.writelines(
                (
                    'set(CMAKE_RULE_LAUNCH_{} "lb-wrapcmd <CMAKE_CURRENT_BINARY_DIR> <TARGET_NAME>"\n'
                    '    CACHE STRING "override")\n'
                ).format(action)
                for action in ("COMPILE", "LINK", "CUSTOM")
            )
            # constrain versions of projects not built in the slot
            if self.project.slot:
                cache.writelines(
                    'set({project}_EXACT_VERSION "{version}" CACHE STRING "")\n'.format(
                        project=p.name, version=to_cmake_version(p.version)
                    )
                    for p in self.project.slot.projects
                    if p.disabled
                )

    def _run(self, cmd, **kwargs):
        # strip special kwargs before command invocation
        cmd_kwargs = {n: v for n, v in kwargs.items() if n not in self.SPECIAL_ARGS}
        cmd_kwargs["cwd"] = str(kwargs.get("cwd", Path.cwd()))
        cmd = [str(c) for c in cmd]
        started = datetime.now()
        result = singularity_run(
            cmd,
            cmd_kwargs["env"],
            cmd_kwargs["cwd"],
            task={
                "task": kwargs.get("step") if kwargs.get("step") == "test" else "build",
                "project": self.project.id(),
                "platform": cmd_kwargs["env"]["BINARY_TAG"],
                "worker_task_id": kwargs.get("worker_task_id"),
            },
            krb_auth=kwargs.get("krb_auth", None),
        )
        if kwargs.get("step") == "build":
            self.build_logs.update(result.build_logs)

        completed = datetime.now()
        step = kwargs.get("step", "script")
        self.reports[step].info(f"running {' '.join(cmd)}")
        self.reports[step].info(f"command exited with code {result.returncode}")
        self.reports[step].started = started.isoformat()
        self.reports[step].completed = completed.isoformat()
        self.reports[step].returncode = result.returncode
        self.reports[step].command = " ".join(quote(a) for a in cmd)
        self.reports[step].stderr = result.stderr
        self.reports[step].stdout = (
            (
                f"#### {self} {step} ####\n"
                f"# Start: {started.isoformat()}\n"
                f"# Command: {' '.join(quote(a) for a in cmd)}\n"
            )
            + result.stdout.decode(errors="surrogateescape")
            + (
                f"# Return code: {result.returncode}\n"
                f"# End: {completed.isoformat()}\n"
            )
        ).encode(errors="surrogateescape")

    def configure(self, **kwargs):
        self._prepare_cache(
            cache_entries=kwargs.get("cache_entries"),
        )
        cmd = [
            "cmake",
            "-S",
            self.project.name,
            "-B",
            self.build_dir,
            "-G",
            kwargs.get("generator", "Ninja"),
            "-C",
            self._cache_preload_file(),
        ]
        # get the toolchain to use
        if self.project.slot and hasattr(self.project.slot, "LCG"):
            LCG_VERSION = self.project.slot.LCG.version
        elif "LCG_VERSION" in kwargs.get("env", {}):
            LCG_VERSION = kwargs["env"]["LCG_VERSION"]
        else:
            out = (
                "\033[0;31mslot configuration error: "
                "version of LCG not defined (required for new "
                "CMake configuration)\033[0m\n"
            )
            raise EnvironmentError(out)

        # When the configuration sets LCG_EXTERNALS_FILE, we have to use the
        # toolchain special/lcg-nightly.cmake
        if "LCG_EXTERNALS_FILE" not in kwargs.get("cache_entries", []):
            toolchain = find_path(
                os.path.join(
                    "lcg-toolchains",
                    "LCG_{}".format(LCG_VERSION),
                    "{}.cmake".format(kwargs["env"]["BINARY_TAG"]),
                ),
                search_path=compute_env(self.project, kwargs.get("env"))
                .get("CMAKE_PREFIX_PATH", "")
                .split(os.pathsep),
            )
        else:
            toolchain = find_path(
                os.path.join("lcg-toolchains", "special", "lcg-nightly.cmake"),
                search_path=compute_env(self.project, kwargs.get("env"))
                .get("CMAKE_PREFIX_PATH", "")
                .split(os.pathsep),
            )

        if not toolchain:
            out = (
                "\033[0;31mslot configuration error: "
                "cannot find toolchain file for {} {}\033[0m\n"
            ).format(LCG_VERSION, kwargs["env"]["BINARY_TAG"])
            raise FileNotFoundError(out)

        cmd.append("-DCMAKE_TOOLCHAIN_FILE=" + toolchain)

        self._run(cmd, step="configure", **kwargs)
        self.build_logs.setdefault("configure", {}).setdefault("configure", []).append(
            {
                "cmd": [str(c) for c in cmd],
                "returncode": self.reports["configure"].returncode,
                "stdout": self.reports["configure"].stdout.decode(
                    errors="surrogateescape"
                ),
                "stderr": self.reports["configure"].stderr.decode(
                    errors="surrogateescape"
                ),
                "started": self.reports["configure"].started,
                "completed": self.reports["configure"].completed,
            }
        )

    def install(self, **kwargs):
        if kwargs.get("relaxed_install"):
            for _file in self.build_dir.rglob("*"):
                if "cmake_install.cmake" in _file.name:
                    with open(_file) as _f:
                        data = _f.read()
                    with open(_file, "w") as _f:
                        _f.write(data.replace("file(INSTALL", "file(INSTALL OPTIONAL"))

        return self._run(
            [
                "cmake",
                "--install",
                self.build_dir,
                "--prefix",
                Path(self.project.name) / "InstallArea" / kwargs["env"]["BINARY_TAG"],
            ],
            step="install",
            **kwargs,
        )

    def build(self, **kwargs):
        """
        Build a project in the current directory using new CMake configuration.

        project has to be a Project instance from lb.nightly.configuration

        Return logging data in the form of a list of messages and executed commands.
        """
        self.configure(**kwargs)
        if self.reports["configure"].returncode:
            # no point trying to build if we failed to configure
            return self.reports, self.build_logs

        cmd = ["cmake", "--build", self.build_dir]
        if "jobs" in kwargs:
            cmd.extend(["-j", str(kwargs["jobs"])])
        if "args" in kwargs:
            cmd.append("--")
            cmd.extend((arg if arg != "-k" else "-k0") for arg in kwargs["args"])
        self._run(cmd, step="build", **kwargs)
        self.install(**kwargs)
        return self.reports, self.build_logs

    def clean(self, **kwargs):
        return self._run(
            [
                "cmake",
                "--build",
                self.build_dir,
                "--target",
                "clean",
            ],
            step="clean",
            **kwargs,
        )

    def test(self, **kwargs):
        cmd = ["ctest", "-T", "test"]
        if "jobs" in kwargs:
            cmd.extend(["-j", str(kwargs["jobs"])])
        self._run(
            cmd,
            step="test",
            cwd=self.build_dir,
            **kwargs,
        )
        return self.reports

    def __str__(self):
        return "CMake (new)"


def is_new_cmake_style(project_dir: Path):
    """
    Check if the project uses the old or new CMake configuration style.
    """
    top_config = project_dir / "CMakeLists.txt"
    if not top_config.exists():
        # no CMakeLists.txt -> it's a CMT project
        return False
    if (project_dir / "toolchain.cmake").exists():
        # custom toolchain file in the sources -> must be old style
        return False
    with open(top_config) as f:
        content = f.read()
    # new style projects do not call "find_package(GaudiProject)"
    return not bool(re.search(r"find_package\s*\(\s*GaudiProject", content))


class make:
    """
    Base class for build tools based on make.
    """

    def __init__(self, project: Project) -> None:
        self.project = project
        if not isinstance(self.project, Project):
            raise TypeError(
                f"expected lb.nightly.configuration.Project instance, "
                f"not {type(project).__name__}"
            )
        self.build_logs = {}

    def _make(self, target, **kwargs):
        """
        Internal function to wrap the call to make for CMT.

        @param target: name of the target to build
        @param jobs: number of parallel build processes [default: 1]
        @param env: dictionary used to override environment variables from the
                    project configuration
        @param args: list of extra arguments to pass to make
        @param make_cmd: command to be used to build [default: ['make']]
        """
        report = Report(f"{__name__}.make")
        jobs = kwargs.get("jobs")

        # "unset" variables set to None
        env = dict(
            (key, value) for key, value in kwargs["env"].items() if value is not None
        )

        cmd_kwargs = {"env": env, "cwd": self.project.baseDir}
        if "stderr" in kwargs:
            cmd_kwargs["stderr"] = kwargs["stderr"]

        cmd = kwargs.get("make_cmd") or "make"
        if isinstance(cmd, str):
            cmd = cmd.split()
        else:
            # make a copy of make_cmd argumens to avoid modifying it
            cmd = list(cmd)

        if jobs:
            cmd.append("-j%d" % jobs)
        cmd.extend(kwargs.get("args", []))
        cmd.append(target)

        ensure_dir(cmd_kwargs["cwd"], report)

        init_project(cmd_kwargs["cwd"])
        report.info("running %s", " ".join(cmd))
        started = datetime.now()
        result = singularity_run(
            cmd,
            cmd_kwargs["env"],
            cmd_kwargs["cwd"],
            task={
                "task": "build",
                "project": self.project.id(),
                "platform": cmd_kwargs["env"].get("BINARY_TAG"),
                "worker_task_id": kwargs.get("worker_task_id"),
            },
            krb_auth=kwargs.get("krb_auth", None),
        )

        completed = datetime.now()
        report.info("command exited with code %d", result.returncode)

        report.stdout = (
            f"#### {self} {target} ####\n"
            f"# Start: {started.isoformat()}\n"
            f"# Command: {' '.join(quote(a) for a in cmd)}\n"
            + result.stdout.decode(errors="surrogateescape")
            + f"# End: {completed.isoformat()}\n"
        ).encode(errors="surrogateescape")
        report.stderr = result.stderr
        report.returncode = result.returncode
        report.started = started.isoformat()
        report.completed = completed.isoformat()
        report.command = " ".join(quote(a) for a in cmd)
        return report, result.build_logs

    def build(self, **kwargs):
        """
        Build a project.
        """
        return self._make("all", **kwargs)

    def clean(self, **kwargs):
        """
        Clean the build products.
        """
        return self._make("clean", **kwargs)

    def test(self, **kwargs):
        """
        Run the tests.
        """
        return self._make("test", **kwargs)

    def __str__(self):
        """
        Conversion to string.
        """
        return "make"


class cmake_old(make):
    def __init__(self, project: Project) -> None:
        self.project = project
        if not isinstance(self.project, Project):
            raise TypeError(
                f"expected lb.nightly.configuration.Project instance, "
                f"not {type(project).__name__}"
            )
        self.reports = {}
        for step in [
            "configure",
            "build",
            "install",
            "clean",
            "test",
            "script",
        ]:
            self.reports[step] = Report(f"{__name__}_{step}.cmake_old")
        self.build_logs = {}

    def _cache_preload_file(self):
        """
        Name of the cache preload file to be passed to CMake.
        """
        return os.path.join(self.project.baseDir, "cache_preload.cmake")

    def _prepare_cache(self, cache_entries=None):
        """
        Prepare the cache_preload.cmake file passed to CMake during the
        configuration.
        """
        # prepare the cache to give to CMake: add the launcher rules commands,
        # followed by what is found passed as argument
        if cache_entries is None:
            cache_entries = []
        elif hasattr(cache_entries, "items"):
            cache_entries = list(cache_entries.items())

        # add the RULE_LAUNCH settings for the build
        launcher_cmd = "lb-wrapcmd <CMAKE_CURRENT_BINARY_DIR> <TARGET_NAME>"
        cache_entries = [
            ("GAUDI_RULE_LAUNCH_%s" % n, launcher_cmd)
            for n in ("COMPILE", "LINK", "CUSTOM")
        ] + cache_entries

        cache_file = self._cache_preload_file()
        ensure_dir(os.path.dirname(cache_file), self.reports["configure"])
        with open(cache_file, "w") as cache:
            cache.writelines(
                [
                    'set(%s "%s" CACHE STRING "override")\n' % item
                    for item in cache_entries
                ]
            )

    def _make(self, target, **kwargs):
        """
        Override basic make call to set the environment variable USE_CMT=1.
        """
        # copy kwargs to be able to change it
        kwargs = dict(kwargs)
        self._prepare_cache(cache_entries=kwargs.pop("cache_entries", None))

        preload_file = os.path.join(os.getcwd(), self._cache_preload_file())
        env = kwargs.get("env", {})
        env.update(
            {
                "USE_CMAKE": "1",
                "USE_MAKE": "1",
            }
        )
        kwargs["env"] = env
        try:
            kwargs["make_cmd"] = kwargs["make_cmd"].get(target)
        except (KeyError, TypeError, AttributeError):
            # no target-specific make_cmd
            pass
        if "relaxed_install" in kwargs:
            del kwargs["relaxed_install"]
        return make._make(self, target, **kwargs)

    def build(self, **kwargs):
        """
        Override the basic build method to call the different targets used in
        CMake builds: configure, all, unsafe-install, post-install.
        """
        kwargs.setdefault("args", [])
        kwargs["args"].insert(0, "BUILDDIR=build")
        logs = {}
        for target in (
            "configure",
            "all",
            "unsafe-install",
            "post-install",
            "clean",
        ):
            self.reports[target], logs[target] = self._make(target, **kwargs)

        # Write configuration logfile fragment for "collect logs" script
        ensure_dir(
            os.path.join(self.project.baseDir, "build", "configure"),
            self.reports["configure"],
        )
        compl = datetime.fromisoformat(self.reports["configure"].completed)
        start = datetime.fromisoformat(self.reports["configure"].started)
        with open(
            os.path.join(
                self.project.baseDir,
                "build",
                "configure",
                "{:%s%f000}-build.log".format(compl),
            ),
            "w",
        ) as conf_log:
            conf_log.writelines(
                self.reports["configure"]
                .stdout.decode(errors="surrogateescape")
                .splitlines(True)[2:-1]
            )
            conf_log.write(
                "\033[0;34mConfiguration completed in {} seconds\033[0m\n".format(
                    (compl - start).total_seconds()
                )
            )
        self.build_logs.setdefault("configure", {}).setdefault("configure", []).append(
            {
                "cmd": (self.reports["configure"].command).split(),
                "returncode": self.reports["configure"].returncode,
                "stdout": "\n".join(
                    self.reports["configure"]
                    .stdout.decode(errors="surrogateescape")
                    .splitlines()[2:-1]
                ),
                "stderr": self.reports["configure"].stderr.decode(
                    errors="surrogateescape"
                ),
                "started": self.reports["configure"].started,
                "completed": self.reports["configure"].completed,
            }
        )
        self.build_logs.update(logs["all"])

        return self.reports, self.build_logs

    def clean(self, **kwargs):
        """
        Override default clean method to call the 'purge' target (more
        aggressive).
        """
        return self._make("purge", **kwargs)

    def test(self, **kwargs):
        """
        Run the tests in a Gaudi/LHCb project.
        """
        kwargs.setdefault("args", [])
        kwargs["args"].insert(0, "BUILDDIR=build")
        if "jobs" in kwargs:
            flag = "-j{}".format(kwargs.pop("jobs"))
            for i, arg in enumerate(kwargs["args"]):
                if arg.startswith("ARGS="):
                    kwargs["args"][i] += " " + flag
                    break
            else:  # (this else matches the for) no ARGS= in args
                kwargs["args"].append(f"ARGS={flag}")
        self.reports["test"], _ = self._make("test", **kwargs)
        return self.reports

    def __str__(self):
        """
        Conversion to string.
        """
        return "CMake (old)"


class cmt(make):
    """
    Class to wrap the build/test semantics for CMT-based projects.
    """

    def _make(self, target, **kwargs):
        """
        Override basic make call to set the environment variable USE_CMT=1.
        """
        env = kwargs.pop("env", {})
        # PWD and CWD may cause troubles to CMT, so we unset them
        env.update({"USE_CMT": "1", "PWD": None, "CWD": None})
        if "CMTROOT" not in env and "make_cmd" not in kwargs:
            kwargs["make_cmd"] = ["cmt", "run", "make"]
        return make._make(self, target, env=env, **kwargs)

    def clean(self, **kwargs):
        """
        Override default clean method to call the 'purge' target (more
        aggressive).
        """
        return self._make("purge", **kwargs)

    def test(self, **kwargs):
        """
        Run the tests in a Gaudi/LHCb project using CMT.
        """
        env = kwargs.get("env", {})
        if "CMTCONFIG" not in env:
            env["CMTCONFIG"] = env.get("BINARY_TAG")
        if "GAUDI_QMTEST_HTML_OUTPUT" not in env:
            bin_dir = os.path.join(
                os.path.abspath(self.project.baseDir), "build", "html"
            )
            env["GAUDI_QMTEST_HTML_OUTPUT"] = bin_dir
        kwargs["env"] = env
        return self._make("test", **kwargs)

    def __str__(self):
        """
        Conversion to string.
        """
        return "CMT"


class cmake:
    """
    Dispatcher to use the old or new style CMake build procedure
    depending on the project.
    """

    def __new__(cls, project: Project):
        return (
            cmake_new(project)
            if is_new_cmake_style(Path(project.name))
            else cmake_old(project)
        )

    def __str__(self):
        """
        Conversion to string.
        """
        return "CMake"
