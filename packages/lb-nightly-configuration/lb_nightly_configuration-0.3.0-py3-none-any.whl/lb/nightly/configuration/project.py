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
import copy
import logging
import os
import re
from hashlib import sha256
from pathlib import Path

from .defaults import DEFAULT_CHECKOUT_METHOD
from .utils import _ContainedList, applyenv, write_patch

__log__ = logging.getLogger(__name__)

# constants
GP_EXP = re.compile(r"gaudi_project\(([^)]+)\)")
HT_EXP = re.compile(r"set\(\s*heptools_version\s+([^)]+)\)")


class Project:
    """
    Describe a project to be checked out, built and tested.
    """

    def __init__(self, name, version, **kwargs):
        """
        @param name: name of the project
        @param version: version of the project as 'vXrY' or 'HEAD', where 'HEAD'
                        means the head version of all the packages
        @param dependencies: optional list of dependencies (as list of project
                             names), can be used to extend the actual (code)
                             dependencies of the project
        @param overrides: dictionary describing the differences between the
                          versions of the packages in the requested projects
                          version and the ones required in the checkout
        @param checkout: callable that can check out the specified project, or
                         tuple (callable, kwargs), with kwargs overriding
                         checkout_opts
        @param checkout_opts: dictionary with extra options for the checkout
                              callable
        @param disabled: if set to True, the project is taken into account only
                         for the configuration
        @param env: override the environment for the project
        @param build_tool: build method used for the project
        @param with_shared: if True, the project requires packing of data
                            generated at build time in the source tree
        @param platform_independent: if True, the project does not require a
                                     build, just the checkout [default: False]
        @param no_test: if True, the tests of the project should not be run
        """
        self.name = name
        self.version = "HEAD" if version.upper() == "HEAD" else version

        # slot owning this project
        self.slot = None

        self.disabled = kwargs.get("disabled", False)
        self.overrides = kwargs.get("overrides", {})
        self._deps = kwargs.get("dependencies", [])
        self.env = kwargs.get("env", [])

        # we need to try setting checkout_opts before checkout, because
        # it could be overridden if checkout is a tuple
        self.checkout_opts = kwargs.get("checkout_opts", {})

        checkout = kwargs.get("checkout") or (
            DEFAULT_CHECKOUT_METHOD
            # for backward compatibility we need to treat "LCG" in a special way
            if name.lower() != "lcg"
            else "lcg"
        )

        if isinstance(checkout, tuple):
            checkout, self.checkout_opts = checkout
        self.checkout = checkout
        self.build_tool = kwargs.get("build_tool", "")

        self.with_shared = kwargs.get("with_shared", False)
        self.platform_independent = kwargs.get("platform_independent", False)
        self.no_test = kwargs.get("no_test", False)
        if "ignore_slot_build_tool" in kwargs:
            self.ignore_slot_build_tool = kwargs["ignore_slot_build_tool"]

        self.build_results = None

    def toDict(self):
        """
        Return a dictionary describing the project, suitable to conversion to
        JSON.
        """
        data = {
            "name": self.name,
            "version": self.version,
            "dependencies": self._deps,
            "overrides": self.overrides,
            "checkout": self.checkout,
            "checkout_opts": self.checkout_opts,
            "disabled": self.disabled,
            "env": self.env,
            "with_shared": self.with_shared,
        }
        if self.platform_independent:
            data["platform_independent"] = True
        if self.no_test:
            data["no_test"] = True
        if hasattr(self, "ignore_slot_build_tool") and self.ignore_slot_build_tool:
            data["ignore_slot_build_tool"] = True
        if (not self.slot or data.get("ignore_slot_build_tool")) and self.build_tool:
            data["build_tool"] = self.build_tool
        return data

    @classmethod
    def fromDict(cls, data):
        """
        Create a Project instance from a dictionary like the one returned by
        Project.toDict().
        """
        return cls(**data)

    def __getstate__(self):
        """
        Allow pickling.
        """
        dct = dict(
            (elem, getattr(self, elem))
            for elem in (
                "name",
                "version",
                "disabled",
                "overrides",
                "_deps",
                "env",
                "checkout",
                "checkout_opts",
                "slot",
                "build_tool",
                "with_shared",
                "platform_independent",
                "no_test",
            )
        )
        return copy.deepcopy(dct)

    def __setstate__(self, state):
        """
        Allow unpickling.
        """
        for key in state:
            setattr(self, key, state[key])

    @property
    def baseDir(self):
        """Name of the project directory (relative to the build directory)."""
        if self.slot and self.slot.with_version_dir:
            upcase = self.name.upper()
            bdir = os.path.join(upcase, "{0}_{1}".format(upcase, self.version))
            __log__.debug(
                "Using file structure with version directory. Base dir=%s" % bdir
            )
            return bdir
        return "%s/" % self.name

    @property
    def enabled(self):
        return not self.disabled

    @enabled.setter
    def enabled(self, value):
        self.disabled = not value

    def dependencies(self):
        """
        Return the dependencies of a checked out project using the information
        retrieved from the configuration files.
        @return: list of used projects (all converted to lowercase, unless we are
        in a slot, in which case the actual casing is used)
        """
        proj_root = self.baseDir

        def fromCMake():
            """
            Helper to extract dependencies from CMake configuration.
            """
            deps = []
            cmake = os.path.join(proj_root, "CMakeLists.txt")
            # arguments to the gaudi_project call
            args = GP_EXP.search(open(cmake).read()).group(1).split()
            if "USE" in args:
                # look for the indexes of the range 'USE' ... 'DATA'
                use_idx = args.index("USE") + 1
                if "DATA" in args:
                    data_idx = args.index("DATA")
                else:
                    data_idx = len(args)
                deps = [p for p in args[use_idx:data_idx:2]]

            # artificial dependency on LCGCMT, if needed
            toolchain = os.path.join(proj_root, "toolchain.cmake")
            if os.path.exists(toolchain) and HT_EXP.search(open(toolchain).read()):
                # we set explicit the version of heptools,
                # so we depend on LCGCMT and LCG
                deps.extend(["LCGCMT", "LCG"])
            if "DATA" in args:
                # if we need data packages, add a dependency on DBASE and PARAM
                deps.extend(["DBASE", "PARAM"])
            return deps

        def fromCMT():
            """
            Helper to extract dependencies from CMT configuration.
            """
            cmt = os.path.join(proj_root, "cmt", "project.cmt")
            # from all the lines in project.cmt that start with 'use',
            # we extract the second word (project name) and convert it to
            # lower case
            return [
                l.split()[1]
                for l in [l.strip() for l in open(cmt)]
                if l.startswith("use")
            ]

        def fromProjInfo():
            """
            Helper to get the dependencies from an info file in the project,
            called 'project.info'.
            The file must be in "config" format (see ConfigParser module) and
            the dependencies must be declared as a comma separated list in
            the section project.

            E.g.:
            [Project]
            dependencies: ProjectA, ProjectB
            """
            import configparser

            config = configparser.ConfigParser()
            config.read(os.path.join(proj_root, "project.info"))
            return [
                proj.strip()
                for proj in config.get("Project", "dependencies").split(",")
            ]

        def fromLHCbProjectYml():
            """
            Helper to get the dependencies from a metadata file in the project,
            called 'lhcbproject.yml'.
            The file (in YAML) must contain a `dependencies` field as a list of
            strings

            E.g.::

                ---
                name: MyProject
                dependencies:
                  - ProjectA
                  - ProjectB
            """
            import yaml

            return yaml.safe_load(open(os.path.join(proj_root, "lhcbproject.yml")))[
                "dependencies"
            ]

        def fromLHCbProjectJson():
            """
            Helper to get the dependencies from a metadata file in the project,
            called 'lhcbproject.json'.
            The file (in JSON) must contain a `dependencies` field as a list of
            strings

            E.g.::

                {
                    "name": "MyProject",
                    "dependencies": [
                        "ProjectA",
                        "ProjectB"
                    ]
                }
            """
            import json

            return json.load(open(os.path.join(proj_root, "lhcbproject.json")))[
                "dependencies"
            ]

        # Try all the helpers until one succeeds
        deps = []
        for helper in (
            fromCMake,
            fromCMT,
            fromLHCbProjectJson,
            fromLHCbProjectYml,
            fromProjInfo,
        ):
            try:
                deps = helper()
                break
            except:
                pass
        else:
            __log__.debug("cannot discover dependencies for %s", self)

        deps = sorted(set(deps + self._deps))
        if self.slot:
            # helper dict to map case insensitive name to correct project names
            names = dict((p.name.lower(), p.name) for p in self.slot.projects)

            def fixNames(iterable):
                "helper to fix the cases of names in dependencies"
                return [names.get(name.lower(), name) for name in iterable]

            deps = fixNames(deps)

        return deps

    def __str__(self):
        """String representation of the project."""
        return "{0}/{1}".format(self.name, self.version)

    def id(self):
        """
        String representing the project instance.

        For standalone Project instances it corresponds to "name/version",
        while for projects in a Slot it is "slot_id/name"
        """
        return (self.slot.id() + "/" + self.name) if self.slot else str(self)

    def __hash__(self):
        return hash(self.id())

    def environment(self, envdict=None):
        """
        Return a dictionary with the environment for the project.

        If envdict is provided, it will be used as a starting point, otherwise
        the environment defined by the slot or by the system will be used.
        """
        # get the initial env from the argument or the system
        if envdict is None:
            envdict = os.environ
        # if we are in a slot, we first process the environment through it
        if self.slot:
            result = self.slot.environment(envdict)
        else:
            # we make a copy to avoid changes to the input
            result = dict(envdict)
        applyenv(result, self.env)
        return result

    def _fixCMakeLists(self, patchfile=None, dryrun=False):
        """
        Fix the 'CMakeLists.txt'.
        """
        from os.path import exists, join

        cmakelists = join(self.baseDir, "CMakeLists.txt")

        if exists(cmakelists):
            __log__.info("patching %s", cmakelists)
            with open(cmakelists) as f:
                data = f.read()
            try:
                # find the project declaration call
                m = GP_EXP.search(data)
                if m is None:
                    __log__.warning(
                        "%s does not look like a Gaudi/CMake "
                        "project, I'm not touching it",
                        self,
                    )
                    return
                args = m.group(1).split()
                # the project version is always the second
                args[1] = self.version

                # fix the dependencies
                if "USE" in args:
                    # look for the indexes of the range 'USE' ... 'DATA'
                    use_idx = args.index("USE") + 1
                    if "DATA" in args:
                        data_idx = args.index("DATA")
                    else:
                        data_idx = len(args)
                    # for each key, get the version (if available)
                    for i in range(use_idx, data_idx, 2):
                        if hasattr(self.slot, args[i]):
                            args[i + 1] = getattr(self.slot, args[i]).version
                # FIXME: we should take into account the declared deps
                start, end = m.start(1), m.end(1)
                newdata = data[:start] + " ".join(args) + data[end:]
            except:  # pylint: disable=W0702
                __log__.error("failed parsing of %s, not patching it", cmakelists)
                return

            if newdata != data:
                if not dryrun:
                    with open(cmakelists, "w") as f:
                        f.write(newdata)
                if patchfile:
                    write_patch(patchfile, data, newdata, cmakelists)

    def _fixCMakeToolchain(self, patchfile=None, dryrun=False):
        """
        Fix 'toolchain.cmake'.
        """
        from os.path import exists, join

        toolchain = join(self.baseDir, "toolchain.cmake")

        if exists(toolchain):
            # case insensitive list of projects
            projs = dict((p.name.lower(), p) for p in self.slot.projects)
            for name in ("heptools", "lcgcmt", "lcg"):
                if name in projs:
                    heptools_version = projs[name].version
                    break
            else:
                # no heptools in the slot
                return
            __log__.info("patching %s", toolchain)
            with open(toolchain) as f:
                data = f.read()
            try:
                # find the heptools version setting
                m = HT_EXP.search(data)
                if m is None:
                    __log__.debug(
                        "%s does not set heptools_version, " "no need to touch", self
                    )
                    return
                start, end = m.start(1), m.end(1)
                newdata = data[:start] + heptools_version + data[end:]
            except:  # pylint: disable=W0702
                __log__.error("failed parsing of %s, not patching it", toolchain)
                return

            if newdata != data:
                if not dryrun:
                    with open(toolchain, "w") as f:
                        f.write(newdata)
                if patchfile:
                    write_patch(patchfile, data, newdata, toolchain)

    def _fixCMake(self, patchfile=None, dryrun=False):
        """
        Fix the CMake configuration of a project, if it exists, and write
        the changes in 'patchfile'.
        """
        self._fixCMakeLists(patchfile, dryrun=dryrun)
        self._fixCMakeToolchain(patchfile, dryrun=dryrun)

    def _fixCMT(self, patchfile=None, dryrun=False):
        """
        Fix the CMT configuration of a project, if it exists, and write
        the changes in 'patchfile'.
        """
        from os.path import exists, join

        project_cmt = join(self.baseDir, "cmt", "project.cmt")

        if exists(project_cmt):
            __log__.info("patching %s", project_cmt)
            with open(project_cmt) as f:
                data = f.readlines()

            # case insensitive list of projects
            projs = dict((p.name.upper(), p) for p in self.slot.projects)

            newdata = []
            for line in data:
                tokens = line.strip().split()
                if len(tokens) == 3 and tokens[0] == "use":
                    if tokens[1] in projs:
                        tokens[1] = projs[tokens[1]].name
                        tokens[2] = ""
                        line = " ".join(tokens) + "\n"
                        __log__.info("result %s", line)
                newdata.append(line)

            if newdata != data:
                if not dryrun:
                    with open(project_cmt, "w") as f:
                        f.writelines(newdata)
                if patchfile:
                    write_patch(patchfile, data, newdata, project_cmt)

        # find the container package
        requirements = join(self.baseDir, self.name + "Release", "cmt", "requirements")
        if not exists(requirements):
            requirements = join(self.baseDir, self.name + "Sys", "cmt", "requirements")

        if exists(requirements):
            __log__.info("patching %s", requirements)
            with open(requirements) as f:
                data = f.readlines()

            used_pkgs = set()

            newdata = []
            for line in data:
                tokens = line.strip().split()
                if len(tokens) >= 3 and tokens[0] == "use":
                    tokens[2] = "*"
                    if len(tokens) >= 4 and tokens[3][0] not in ("-", "#"):
                        used_pkgs.add("{3}/{1}".format(*tokens))
                    else:
                        used_pkgs.add(tokens[1])
                    line = " ".join(tokens) + "\n"
                newdata.append(line)

            for added_pkg in set(self.overrides.keys()) - used_pkgs:
                if "/" in added_pkg:
                    hat, added_pkg = added_pkg.rsplit("/", 1)
                else:
                    hat = ""
                newdata.append("use {0} * {1}\n".format(added_pkg, hat))

            if not dryrun:
                with open(requirements, "w") as f:
                    f.writelines(newdata)

            if patchfile:
                write_patch(patchfile, data, newdata, requirements)

    def _fixProjectConfigJSON(self, patchfile=None, dryrun=False):
        """
        Fix 'dist-tools/projectConfig.json'.
        """
        import codecs
        import json
        from os.path import exists, join

        configfile = join(self.baseDir, "dist-tools", "projectConfig.json")

        if exists(configfile):
            __log__.info("patching %s", configfile)
            with codecs.open(configfile, encoding="utf-8") as f:
                data = f.read()

            config = json.loads(data)
            data = data.splitlines(True)

            config["version"] = self.version

            # case insensitive list of projects
            projs = dict((p.name.lower(), p.version) for p in self.slot.projects)
            # update project versions (if defined
            if "used_projects" in config:
                for dep in config["used_projects"]["project"]:
                    dep[1] = projs.get(dep[0].lower(), dep[1])

            if "heptools" in config:
                for name in ("heptools", "lcgcmt", "lcg"):
                    if name in projs:
                        config["heptools"]["version"] = projs[name]
                        break

            newdata = json.dumps(config, indent=2).splitlines(True)

            if not dryrun:
                with codecs.open(configfile, "w", encoding="utf-8") as f:
                    f.writelines(newdata)

            if patchfile:
                write_patch(patchfile, data, newdata, configfile)

    def patch(self, patchfile=None, dryrun=False):
        """
        Modify dependencies and references of the project to the other projects
        in a slot.

        @param patchfile: a file object where the applied changes can be
                          recorded in the form of "patch" instructions.

        @warning: It make sense only for projects within a slot.
        """
        if not self.slot:
            raise ValueError("project %s is not part of a slot" % self)

        self._fixCMake(patchfile, dryrun=dryrun)
        self._fixCMT(patchfile, dryrun=dryrun)
        self._fixProjectConfigJSON(patchfile, dryrun=dryrun)

    def hash(self, platform: str = "") -> str:
        """
        Compute a unique id for the specific project version of the code.

        The hash is a `sha256` sum of the commit ids used for the checkout
        of the project, unless the project is disabled, in which case we use
        only name and version.

        If `platform` is specified, it is included in the hash and if the
        project is attached to a slot and the dependencies are taken into
        account too.
        """
        # hash is computed as sha256 sum of
        # - commit or id
        # - 'mr_commit's
        hash = sha256()

        if self.disabled:
            hash.update(f"{self.name}/{self.version}".encode())
        else:
            hash.update((self.checkout_opts.get("commit") or self.id()).encode())
            for _, mr_commit in self.checkout_opts.get("merges", []):
                hash.update(mr_commit.encode())

        if platform:
            # include the platform in the hash
            hash.update(platform.encode())
            if self.slot:
                # dependencies are considered if we are in a slot
                for dep in [
                    getattr(self.slot, dep)
                    for dep in self.dependencies()
                    if hasattr(self.slot, dep)
                ]:
                    hash.update(dep.hash(platform).encode())

        return hash.hexdigest()

    def artifacts(self, stage, platform=""):
        """
        Returns the name of the artifacts zip file for a project.

        @param stage: string describing type of artifacts (i.e. checkout,
                        build/tests for given platform)
        @param platform: string describing the platform (required for build
                        and test stage, not allowed for checkout)

        Raises ValueError if:
         - stage is not checkout, build, or test,
         - platform is not specified for build and test
         - platform is specified for checkout
        """

        if stage not in ["checkout", "build", "test"]:
            raise ValueError("Unrecognised stage of the artifact")
        elif stage == "checkout" and platform != "":
            raise ValueError("Platform cannot be set for checkout")
        elif stage in ["build", "test"] and not platform:
            raise ValueError("Platform must be set for build and test")

        if stage == "checkout":
            path = Path(stage)
            hash = self.hash()
            return str(path / self.name / hash[:2] / (hash + ".zip"))

        pid = self.id()
        if self.slot:
            # if project is within a slot, the path should start with:
            # flavour/slot/build_id
            path = pid.rsplit("/", 1)[0]
            slotname = self.slot.name
            slotbid = str(self.slot.build_id)
        else:
            path = ""
            slotname = ""
            slotbid = ""

        filename = self.name

        if stage == "build":

            path = os.path.join(path, "packs", platform)
            filename = ".".join(
                list(
                    filter(
                        None,
                        [
                            filename,
                            self.version,
                            slotname,
                            slotbid,
                            platform,
                            "zip",
                        ],
                    )
                )
            )
        elif stage == "test":
            path = os.path.join(path, "tests", platform)
            filename = ".".join(
                [
                    filename,
                    "zip",
                ]
            )

        return os.path.join(path, filename)

    def get_deployment_directory(self) -> Path:
        from . import lbnightly_settings

        return Path(lbnightly_settings().installations.path) / self.id()


class ProjectsList(_ContainedList):
    """
    Helper class to handle a list of projects bound to a slot.
    """

    __type__ = Project
    __container_member__ = "slot"


class Package:
    """
    Describe a package to be checked out.
    """

    def __init__(self, name, version, **kwargs):
        """
        @param name: name of the package
        @param version: version of the package as 'vXrY' or 'HEAD'
        @param checkout: callable that can check out the specified package
        @param checkout_opts: dictionary with extra options for the checkout
                              callable
        """
        self.name = name
        if version.lower() == "head":
            version = "head"
        self.version = version
        self.container = None
        self.checkout_opts = kwargs.get("checkout_opts", {})
        checkout = kwargs.get("checkout") or DEFAULT_CHECKOUT_METHOD
        if isinstance(checkout, tuple):
            checkout, self.checkout_opts = checkout
        self.checkout = checkout

    @property
    def slot(self):
        return self.container.slot if self.container else None

    def toDict(self):
        """
        Return a dictionary describing the package, suitable to conversion to
        JSON.
        """
        data = {
            "name": self.name,
            "version": self.version,
            "checkout": self.checkout,
            "checkout_opts": self.checkout_opts,
        }
        if self.container:
            data["container"] = self.container.name
        return data

    def __getstate__(self):
        """
        Allow pickling.
        """
        dct = dict(
            (elem, getattr(self, elem))
            for elem in ("name", "version", "checkout_opts", "container")
        )
        dct["checkout"] = self.checkout
        return copy.deepcopy(dct)

    def __setstate__(self, state):
        """
        Allow unpickling.
        """
        for key in state:
            setattr(self, key, state[key])

    @property
    def baseDir(self):
        """Name of the package directory (relative to the build directory)."""
        if self.container:
            return os.path.join(self.container.baseDir, self.name, self.version)
        else:
            return os.path.join(self.name, self.version)

    def getVersionLinks(self):
        """
        Return a list of version aliases for the current package (only if the
        requested version is not vXrY[pZ]).
        """
        if re.match(r"v\d+r\d+(p\d+)?$", self.version):
            return []
        base = self.baseDir
        aliases = ["v999r999"]
        if os.path.exists(os.path.join(base, "cmt", "requirements")):
            for l in open(os.path.join(base, "cmt", "requirements")):
                l = l.strip()
                if l.startswith("version"):
                    version = l.split()[1]
                    aliases.append(version[: version.rfind("r")] + "r999")
                    break
        return aliases

    def __str__(self):
        """String representation of the package."""
        return "{0}/{1}".format(self.name, self.version)

    def id(self, show_container=True):
        """
        String representing the package instance.

        For standalone Package instances it corresponds to "name/version",
        while for projects in a DataProject it is "<project.id()>[name]"
        """
        return (
            f"{self.container.id()}/{self.name}"
            if self.container and show_container
            else self.container.id().replace(self.container.name, self.name)
            if self.container and not show_container
            else str(self)
        )

    def hash(self) -> str:
        """
        Compute a unique id for the specific project version of the code.

        The hash is a `sha256` sum of the commit ids used for the checkout
        of the data package.
        """
        # hash is computed as sha256 sum of
        # - version name (as it affects the content of the checkout) + commit
        #   - or id
        # - 'mr_commit's
        hash = sha256()
        if "commit" in self.checkout_opts:
            hash.update(self.version.encode())
            hash.update(self.checkout_opts["commit"].encode())
        else:
            hash.update(self.id().encode())
        for _, mr_commit in self.checkout_opts.get("merges", []):
            hash.update(mr_commit.encode())

        return hash.hexdigest()

    def artifacts(self, stage="checkout", platform=""):
        """
        Returns the name of the artifacts zip file for a package.

        @param stage: kept for compatibility with Project, the only value
                      allowed is "checkout"
        @param platform: kept for compatibility with Project, must not be set

        Raises ValueError if:
         - stage is not checkout
         - platform is specified
        """
        if stage != "checkout" or platform:
            raise ValueError("Only 'checkout' stage allowed for DataProject.artifacts")

        path = Path(stage)
        hash = self.hash()
        return str(path / self.name / hash[:2] / (hash + ".zip"))

    def get_deployment_directory(self) -> Path:
        from . import lbnightly_settings

        return Path(lbnightly_settings().installations.path) / self.id()


class PackagesList(_ContainedList):
    """
    Helper class to handle a list of projects bound to a slot.
    """

    __type__ = Package
    __container_member__ = "container"


class DataProject(Project):
    """
    Special Project class for projects containing only data packages.
    """

    ignore_slot_build_tool = True
    build_tool = "no_build"

    def __init__(self, name, packages=None, **kwargs):
        """
        Initialize the instance with name and list of packages.
        """
        # we use 'None' as version just to comply with Project.__init__, but the
        # version is ignored
        Project.__init__(self, name, "None", **kwargs)
        # data projects are platform independent by definition
        self.platform_independent = True
        # data projects cannot be tested by definition
        self.no_test = True
        if packages is None:
            packages = []
        self._packages = PackagesList(self, packages)

    def toDict(self):
        """
        Return a dictionary describing the data project, suitable to conversion
        to JSON.
        """
        data = {
            "name": self.name,
            "version": self.version,
            "checkout": "ignore",
            "disabled": False,
            "platform_independent": True,
            "no_test": True,
        }
        return data

    def __getstate__(self):
        """
        Allow pickling.
        """
        dct = Project.__getstate__(self)
        dct["_packages"] = self._packages
        dct["checkout"] = None
        return copy.deepcopy(dct)

    def __setstate__(self, state):
        """
        Allow unpickling.
        """
        for key in state:
            setattr(self, key, state[key])

    def __str__(self):
        """String representation of the project."""
        return self.name

    @property
    def baseDir(self):
        """Name of the package directory (relative to the build directory)."""
        return self.name.upper()

    @property
    def packages(self):
        "List of contained packages"
        return self._packages

    def __getattr__(self, name):
        """
        Get the project with given name in the slot.
        """
        try:
            return self._packages[name]
        except KeyError:
            raise AttributeError(
                "%r object has no attribute %r" % (self.__class__.__name__, name)
            )

    def hash(self, platform: str = "") -> str:
        """
        Compute a unique id for the specific project version of the code.

        The hash is a `sha256` sum of the hashes of the contained packages.

        The `platform` argument is ignored but kept for compatibility with
        he base class.
        """
        # hash is computed as sha256 sum of
        # - for each package
        #   - package hash
        hash = sha256()

        for package in sorted(self.packages, key=lambda p: p.name):
            hash.update(package.hash().encode())

        return hash.hexdigest()

    def artifacts(self, stage="checkout", platform=""):
        """
        Returns the name of the artifacts zip file for a data project.

        @param stage: kept for compatibility with Project, the only value
                      allowed is "checkout"
        @param platform: kept for compatibility with Project, must not be set

        Raises ValueError if:
         - stage is not checkout
         - platform is specified
        """
        if stage != "checkout" or platform:
            raise ValueError("Only 'checkout' stage allowed for DataProject.artifacts")

        path = Path(stage)
        hash = self.hash()

        return str(path / self.name / hash[:2] / (hash + ".zip"))


class DBASE(DataProject):
    def __init__(self, **kwargs):
        DataProject.__init__(self, "DBASE", **kwargs)

    def __hash__(self):
        return hash(self.id())


class PARAM(DataProject):
    def __init__(self, **kwargs):
        DataProject.__init__(self, "PARAM", **kwargs)

    def __hash__(self):
        return hash(self.id())


STANDARD_CONTAINERS = {
    "DBASE": DBASE,
    "PARAM": PARAM,
}
