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
import re
from collections import OrderedDict
from pathlib import Path

from .defaults import DEFAULT_BUILD_TOOL
from .project import STANDARD_CONTAINERS, DataProject, Package, Project, ProjectsList
from .utils import applyenv

__log__ = logging.getLogger(__name__)

_slot_factories = set()


def slot_factory(f):
    """
    Decorator used to flag a function as a Slot factory to correctly
    trace the module defining a slot.
    """
    global _slot_factories
    _slot_factories.add(f.__name__)
    return f


class Slot:
    """
    Generic nightly build slot.
    """

    __slots__ = (
        "_name",
        "projects",
        "env",
        "build_tool",
        "disabled",
        "desc",
        "platforms",
        "error_exceptions",
        "warning_exceptions",
        "preconditions",
        "cache_entries",
        "build_id",
        "no_patch",
        "with_version_dir",
        "no_test",
        "deployment",
        "metadata",
        "_source",
    )
    __projects__ = []
    __env__ = []

    def __init__(self, name, projects=None, **kwargs):
        """
        Initialize the slot with name and optional list of projects.

        @param name: name of the slot
        @param projects: (optional) list of Project instances
        @param env: (optional) list of strings ('name=value') used to modify the
                    environment for the slot
        @param disabled: if True the slot should not be used in the nightly
                         builds
        @param desc: description of the slot
        @param platforms: list of platform ids the slot should be built for
        @param warning_exceptions: list of regex of warnings that should be
                                   ignored
        @param error_exceptions: list of regex of errors that should be ignored
        @param cache_entries: dictionary of CMake cache variables to preset
        @param build_id: numeric id for the build
        @param no_patch: if set to True, sources will not be patched (default to
                         False) Kept for retro-compatibility
        @param with_version_dir: if set to True, sources will be checkout in
                                 the path: Project/Project_version
        @param no_test: if set to True, tests should not be run for this slot)
        @param deployment: list of deployment destinations (strings)
        @param metadata: dictionary with extra information, e.g. for the dashboard
        """
        self._name = name
        self.build_id = kwargs.get("build_id", 0)

        if projects is None:
            projects = self.__projects__
        self.projects = ProjectsList(self, projects)
        self.env = kwargs.get("env", list(self.__env__))
        self.build_tool = kwargs.get("build_tool") or DEFAULT_BUILD_TOOL
        self.disabled = kwargs.get("disabled", False)
        desc = kwargs.get("desc")
        if desc is None:
            desc = (self.__doc__ or "<no description>").strip()
        self.desc = desc

        self.platforms = kwargs.get("platforms", [])
        if isinstance(self.platforms, str):
            self.platforms = [self.platforms]
        for p in self.platforms:
            assert re.match(r"^[0-9a-z_+]+-[0-9a-z_]+-[0-9a-z_+]+-[0-9a-z_+]+$", p), (
                "invalid platform: %r" % p
            )

        self.error_exceptions = kwargs.get("error_exceptions", [])
        self.warning_exceptions = kwargs.get("warning_exceptions", [])

        self.preconditions = kwargs.get("preconditions", [])

        self.cache_entries = kwargs.get("cache_entries", {})

        self.no_patch = kwargs.get("no_patch", False)
        self.with_version_dir = kwargs.get("with_version_dir", False)
        self.no_test = kwargs.get("no_test", False)

        self.deployment = kwargs.get("deployment", [])

        self.metadata = kwargs.get("metadata", {})

        # get the name of the Python module calling the constructor,
        # excluding irrelevant frames
        import inspect

        caller = inspect.currentframe().f_back
        while caller.f_code.co_name in _slot_factories:
            caller = caller.f_back
        self._source = caller.f_globals["__name__"]

    def toDict(self):
        """
        Return a dictionary describing the slot, suitable to conversion to JSON.
        """
        from itertools import chain

        data = {
            "slot": self.name,
            "description": self.desc,
            "projects": [proj.toDict() for proj in self.projects],
            "disabled": self.disabled,
            "build_tool": self.build_tool,
            "env": self.env,
            "error_exceptions": self.error_exceptions,
            "warning_exceptions": self.warning_exceptions,
            "preconditions": self.preconditions,
            "build_id": self.build_id,
        }
        if self.cache_entries:
            data["cmake_cache"] = self.cache_entries
        if self.no_patch:
            data["no_patch"] = True
        if self.with_version_dir:
            data["with_version_dir"] = True
        if self.no_test:
            data["no_test"] = True
        if self.deployment:
            data["deployment"] = self.deployment
        if self.metadata:
            data["metadata"] = self.metadata

        pkgs = list(
            chain.from_iterable(
                [pack.toDict() for pack in cont.packages]
                for cont in self.projects
                if isinstance(cont, DataProject)
            )
        )
        data["packages"] = pkgs
        data["platforms"] = self.platforms

        return data

    @classmethod
    @slot_factory
    def fromDict(cls, data):
        """
        Create a Slot instance from a dictionary like the one returned by
        Slot.toDict().
        """
        containers = {}
        for pkg in data.get("packages", []):
            container = pkg.get("container", "DBASE")
            if container not in containers:
                if container in STANDARD_CONTAINERS:
                    containers[container] = STANDARD_CONTAINERS[container]()
                else:
                    containers[container] = DataProject(container)
            container = containers[container]
            pkg = Package(
                pkg["name"],
                pkg["version"],
                checkout=pkg.get("checkout"),
                checkout_opts=pkg.get("checkout_opts", {}),
            )
            container.packages.append(pkg)

        projects = [
            Project.fromDict(prj)
            if prj["name"] not in containers
            else containers[prj["name"]]
            for prj in data.get("projects", [])
        ]
        if containers and not projects:
            projects = list(containers.values())
        slot = cls(
            name=data.get("slot", None),
            projects=projects,
            env=data.get("env", []),
            desc=data.get("description"),
            disabled=data.get("disabled", False),
            deployment=data.get("deployment", []),
            metadata=data.get("metadata", {}),
        )
        slot.platforms = data.get("platforms", data.get("default_platforms", []))

        if data.get("USE_CMT"):
            slot.build_tool = "cmt"
        if "build_tool" in data:
            slot.build_tool = data["build_tool"]

        slot.error_exceptions = data.get("error_exceptions", [])
        slot.warning_exceptions = data.get("warning_exceptions", [])
        slot.preconditions = data.get("preconditions", [])

        slot.cache_entries = data.get("cmake_cache", {})

        slot.build_id = data.get("build_id", 0)

        slot.no_patch = data.get("no_patch", False)
        slot.with_version_dir = data.get("with_version_dir", False)
        slot.no_test = data.get("no_test", False)

        return slot

    def __getstate__(self):
        """
        Allow pickling.
        """
        return self.toDict()

    def __setstate__(self, data):
        """
        Allow unpickling.
        """
        containers = {}
        for pkg in data.get("packages", []):
            container = pkg.get("container", "DBASE")
            if container not in containers:
                if container in STANDARD_CONTAINERS:
                    containers[container] = STANDARD_CONTAINERS[container]()
                else:
                    containers[container] = DataProject(container)
            container = containers[container]
            pkg = Package(
                pkg["name"],
                pkg["version"],
                checkout=pkg.get("checkout"),
                checkout_opts=pkg.get("checkout_opts", {}),
            )
            container.packages.append(pkg)

        if data.get("USE_CMT"):
            self.build_tool = "cmt"
        if "build_tool" in data:
            self.build_tool = data["build_tool"]
        self.platforms = data.get("platforms", data.get("default_platforms", []))
        self.name = data.get("slot", None)
        projects = [
            Project.fromDict(prj)
            if prj["name"] not in containers
            else containers[prj["name"]]
            for prj in data.get("projects", [])
        ]
        if containers and not projects:
            projects = list(containers.values())
        self.projects = ProjectsList(self, projects)
        self.env = data.get("env", [])
        self.desc = data.get("description")
        self.disabled = data.get("disabled", False)
        self.deployment = data.get("deployment", [])
        self.metadata = data.get("metadata", {})
        self.error_exceptions = data.get("error_exceptions", [])
        self.warning_exceptions = data.get("warning_exceptions", [])
        self.preconditions = data.get("preconditions", [])
        self.cache_entries = data.get("cmake_cache", {})
        self.build_id = data.get("build_id", 0)
        self.no_patch = data.get("no_patch", False)
        self.with_version_dir = data.get("with_version_dir", False)
        self.no_test = data.get("no_test", False)

    def _clone(self, new_name):
        """
        Return a new instance configured as this one except for the name.
        """
        return Slot(new_name, projects=self.projects)

    @property
    def name(self):
        """
        Name of the slot.
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Change the name of the slot, keeping the slots global list in sync.
        """
        self._name = value

    @property
    def enabled(self):
        return not self.disabled

    @enabled.setter
    def enabled(self, value):
        self.disabled = not value

    def __getattr__(self, name):
        """
        Get the project with given name in the slot.
        """
        try:
            return self.projects[name]
        except KeyError:
            raise AttributeError(
                "%r object has no attribute %r" % (self.__class__.__name__, name)
            )

    def __delattr__(self, name):
        """
        Remove a project from the slot.
        """
        self.projects.remove(self.projects[name])

    def __dir__(self):
        """
        Return the list of names of the attributes of the instance.
        """
        return list(self.__dict__.keys()) + [proj.name for proj in self.projects]

    def __str__(self):
        """String representation of the slot."""
        return (
            "{0}.{1}".format(self.name, self.build_id) if self.build_id else self.name
        )

    def id(self):
        """
        String representing the slot instance.

        >>> s = Slot('test', build_id=10)
        >>> s.id()
        'nightly/test/10'
        >>> s = Slot('another')
        >>> s.flavour = 'testing'
        >>> s.id()
        'testing/another/0'
        """
        return "/".join(
            [
                self.flavour,
                self.name,
                str(self.build_id),
            ]
        )

    def __hash__(self):
        return hash(self.id())

    @property
    def activeProjects(self):
        """
        Generator yielding the projects in the slot that do not have the
        disabled property set to True.
        """
        for p in self.projects:
            if p.enabled:
                yield p

    def patch(self, patchfile=None, dryrun=False):
        """
        Patch all active projects in the slot to have consistent dependencies.
        """
        if self.no_patch:
            raise ValueError("slot %s cannot be patched (no_patch=True)" % self)
        for project in self.activeProjects:
            project.patch(patchfile, dryrun=dryrun)

    def dependencies(self, projects=None):
        """
        Dictionary of dependencies between projects (only within the slot).
        """
        deps = self.fullDependencies()
        if projects:
            for unwanted in set(deps) - set(projects):
                deps.pop(unwanted)
        for key in deps:
            deps[key] = [val for val in deps[key] if val in deps]
        return deps

    def fullDependencies(self):
        """
        Dictionary of dependencies of projects (also to projects not in the
        slot).
        """
        return OrderedDict([(p.name, p.dependencies()) for p in self.projects])

    def dependencyGraph(self, keep_extern_nodes=False):
        """
        Return a networkx.OrderedDiGraph of the dependencies between projects.

        If keep_extern_nodes is False, only the projects in the slot are considered,
        otherwise we get also dependencies outside the slot.

        The edges go from dependee to depender (e.g. Gaudi -> LHCb).
        """
        from networkx import OrderedDiGraph

        if keep_extern_nodes:
            deps = self.fullDependencies()
        else:
            deps = self.dependencies()
        return OrderedDiGraph((d, p) for p in deps for d in deps[p])

    def environment(self, envdict=None):
        """
        Return a dictionary with the environment for the slot.

        If envdict is provided, it will be used as a starting point, otherwise
        the environment defined by the system will be used.
        """
        result = dict(os.environ) if envdict is None else dict(envdict)
        applyenv(result, self.env)
        # ensure that the current directory is first in the CMake and CMT
        # search paths
        from os import pathsep

        curdir = os.getcwd()
        for var in ("CMTPROJECTPATH", "CMAKE_PREFIX_PATH"):
            if var in result:
                result[var] = pathsep.join([curdir, result[var]])
            else:
                result[var] = curdir
        return result

    def _projects_by_deps(self, projects=None):
        from .Common import sortedByDeps

        deps = self.dependencies(projects=projects)
        return [
            project
            for project in [
                getattr(self, project_name) for project_name in sortedByDeps(deps)
            ]
            if project.enabled
        ]

    @property
    def flavour(self):
        return self.metadata.get(
            "flavour",
            "release"
            if self.name in ("lhcb-release", "release")
            else "testing"
            if self.name.startswith("test-")
            else "nightly",
        )

    @flavour.setter
    def flavour(self, value):
        self.metadata["flavour"] = value

    def get_deployment_directory(self) -> Path:
        from . import lbnightly_settings

        return Path(lbnightly_settings().installations.path) / self.id()

    def artifacts(self, stage, platform=""):
        """
        Returns the name of the artifacts zip file for a slot.

        @param stage: string describing type of artifacts, only "deployment_dir"
                      can be used for slots (Project and Package have more options)
        @param platform: kept for compatibility with Project.artifacts interface,
                         must be empty for slots

        Raises ValueError if:
         - stage is not deployment_dir,
         - platform is specified
        """

        if stage != "deployment_dir":
            raise ValueError("Unrecognised stage of the artifact")
        elif platform != "":
            raise ValueError("Platform cannot be set for deployment_dir")

        return f"{self.id()}/{stage}.zip"
