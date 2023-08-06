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
__version__ = "0.3.1"

import json
import logging
import os
import re
import sys
from collections import namedtuple
from urllib.parse import urlsplit, urlunsplit
from urllib.request import urlopen

from .project import DBASE, PARAM, DataProject, Package, Project
from .slot import Slot, slot_factory
from .utils import configToString, save


def service_config(config_file=None, silent=False):
    """
    Returns dictionary with configs required to use external
    services like couchdb, rabbitmq or gitlab. All the
    information needed (urls, ports, tokens, username,
    passwords, etc.) should be stored in yaml file provided as an argument
    or the agreed file from the private directory will be taken.
    If yaml is not correct or does not exists, exception is raised, unlsess
    silent is True, in which case None is returned.
    """
    import yaml

    if config_file is None:
        # if configuration file is not provided
        # try to take secrets.yaml from private directory
        if os.environ.get("PRIVATE_DIR"):
            config_file = os.path.join(os.environ["PRIVATE_DIR"], "secrets.yaml")
        else:
            config_file = os.path.expanduser(
                os.path.join("~", "private", "secrets.yaml")
            )

    try:
        with open(config_file) as f:
            config = yaml.safe_load(f)
    except (yaml.YAMLError, FileNotFoundError) as exc:
        if silent:
            return None
        logging.warning(f"Could not get the configuration for this service: {exc}")
        raise

    return config


def lbnightly_settings(secrets_yaml="./secrets.yaml"):
    """
    Returns configurator.config.Config object containing the settings
    needed for lb-nightly services, merged from the following sources:
     * hardcoded defaults
     * system level `secrets.yaml` expected to be found in `$PRIVATE_DIR`
       or `~/private/`
     * user level yaml file provided as an argument, by default secrets.yaml
       from current directory is taken if exists.

    Data can be retrieved using dot notation (`lbnightly_settings().couchdb.url`)
    or like from a dictionary (`lbnightly_settings()['couchdb']['url']`).

    One can also get the plain dictionary with settings by calling:
    `lbnightly_settings().data`.

    Raises AttributeError or KeyError if a requested setting is not found
    (depending on the way of access).
    """
    from configurator import Config

    # FIXME: the values defined below are meant to be sensisble defaults
    defaults = Config(
        {
            "couchdb": {"url": "http://localhost:8080/couchdb/nightly-builds"},
            "rabbitmq": {"url": "amqp://guest:guest@localhost:5672"},
            "mysql": {"url": "db+mysql://"},
            "artifacts": {
                "uri": "http://localhost:8081/repository/nightly_builds_artifacts/"
            },
            "logs": {"uri": "http://localhost:8081/repository/nightly_builds_logs/"},
            "elasticsearch": {"uri": "http://localhost:9200"},
            "installations": {"path": "/cvmfs/lhcbdev.cern.ch/nightlies"},
        }
    )
    system = Config.from_path(
        os.path.join(
            os.environ.get(
                "PRIVATE_DIR", os.path.join(os.path.expanduser("~"), "private")
            ),
            "secrets.yaml",
        ),
        optional=True,
    )
    user = Config.from_path(secrets_yaml, optional=True)

    return defaults + system + user


def loadConfig(module=None):
    """
    Load all slots from a config module.
    """
    from importlib import import_module

    import git

    orig_path = list(sys.path)
    if module is None:
        module_name, attribute = "lhcbnightlyconf", "slots"
    elif ":" in module:
        module_name, attribute = module.split(":", 1)
    else:
        module_name, attribute = module, "slots"
    sys.path.insert(0, os.curdir)
    sys.path.insert(0, "configs")
    m = import_module(module_name)
    try:  # to get the commit id of the config directory
        config_id = (
            git.Repo(m.__path__[0], search_parent_directories=True)
            .rev_parse("HEAD")
            .hexsha
        )
    except git.GitError:
        config_id = None
    slot_list = getattr(m, attribute)
    logging.debug("using explicit configuration")
    slot_dict = {}
    for slot in slot_list:
        assert (
            slot.name not in slot_dict
        ), "Slot {} defined in 2 places: {} and {}".format(
            slot.name, slot_dict[slot.name]._source, slot._source
        )
        if config_id:
            slot.metadata["config_id"] = config_id
        slot_dict[slot.name] = slot
    sys.path = orig_path
    return slot_dict


KeyTuple = namedtuple("KeyTuple", ["flavour", "name", "id", "project"])
KeyTuple.__str__ = lambda self: "/".join(str(i) for i in self if i is not None)


def _parse_key(key):
    """
    Parse a key like "[flavour/]slotname[/build_id][/project]" to its parts.

    Returns a named tuple with the elements.

    NOTE: if `flavour/` is present, there must be also at least one of `/build_id`
          or `/project`, as the string "a/b" is always interpreted as "slot/project"
    """
    # defaults for optional entries
    flavour, build_id, project = "nightly", "0", None
    name = None  # used to flag invalid keys

    # we do max 3 splits because project may be in fact
    # a package inside container, e.g. DBASE/WG/CharmConfig
    tokens = key.split("/", maxsplit=3)
    if len(tokens) == 1:  # only slot name
        name = tokens[0]
    elif len(tokens) == 2:  # slot/build_id or slot/project
        name = tokens[0]
        if tokens[1].isdigit():
            build_id = tokens[1]
        else:
            project = tokens[1]
    elif len(tokens) == 3:  # f/s/b, f/s/p or s/b/p
        if tokens[2].isdigit():  # f/s/b
            flavour, name, build_id = tokens
        elif tokens[1].isdigit():  # s/b/p
            name, build_id, project = tokens
        else:  # f/s/p
            flavour, name, project = tokens
    elif len(tokens) == 4:
        if tokens[2].isdigit():
            flavour, name, build_id, project = tokens

    if not name:
        raise ValueError("%r is not a valid key" % key)

    return KeyTuple(flavour, name, int(build_id), project)


def get(key):
    """
    Get the instance identified by a key like
    "[flavour/]slotname/build_id[/project]" from the database.
    """
    flavour, slot, build_id, project = _parse_key(key)

    if build_id <= 0:
        raise ValueError("build_id must be specified and > 0")

    db_doc_id = ":".join((flavour, slot, str(build_id)))

    try:
        db_url = service_config(silent=True)["couchdb"]["url"]
    except (KeyError, TypeError):
        # FIXME: this is meant to be a sensible default
        db_url = "http://localhost:8080/couchdb/nightly-builds"

    parts = urlsplit(db_url)
    if "@" in parts.netloc:
        # strip authentication details from url
        netloc = parts.netloc.rsplit("@", 1)[-1]
        db_url = urlunsplit(
            (parts.scheme, netloc, parts.path, parts.query, parts.fragment)
        )

    slot = Slot.fromDict(json.load(urlopen("/".join((db_url, db_doc_id))))["config"])
    if slot.flavour != flavour:
        logging.warning(
            f"inconsistent slot flavour: fixing the Slot instance by setting the flavour to: {flavour}"
        )
        slot.flavour = flavour

    if project is None:
        return slot
    try:
        return slot.projects[project]
    except KeyError as no_proj_err:
        # check if the `project` is amongst names of the packages
        try:
            # strip the container name
            package = project.split("/", 1)[1]
            return next(
                dp.packages[package]
                for dp in slot.projects
                if isinstance(dp, DataProject) and package in dp.packages
            )
        except (StopIteration, IndexError):
            raise no_proj_err


def check_slot(slot):
    """
    Check that a slot configuration is valid.
    """
    good = True
    log = logging.getLogger(slot.name)

    def check_type(field_name, types, value=None):
        if value is None:
            value = getattr(slot, field_name)
        if not isinstance(value, types):
            log.error(
                "invalid %s type: found %s, expected any of [%s]",
                field_name,
                type(value).__name__,
                ", ".join(t.__name__ for t in types),
            )
            return False
        return True

    def check_list_of_strings(field_name, name, regex):
        good = check_type(field_name, (list, tuple))
        for x in getattr(slot, field_name):
            if check_type(name, (str,), x):
                if not re.match(regex, x):
                    log.error("invalid %s value: %r", name, x)
                    good = False
            else:
                good = False
        return good

    for field_name in ("warning_exceptions", "error_exceptions"):
        good &= check_type(field_name, (list, tuple))
        for x in getattr(slot, field_name):
            try:
                re.compile(x)
            except Exception as err:
                good = False
                log.error("%s: invalid value %r: %s", field_name, x, err)

    good &= check_list_of_strings(
        "platforms", "platform", r"^[a-z0-9_+]+-[a-z0-9_]+-[a-z0-9_+]+-[a-z0-9_+]+$"
    )
    good &= check_list_of_strings("env", "env setting", r"^[a-zA-Z_][a-z0-9A-Z_]*=")

    return good


def check_config():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "module",
        nargs="?",
        help="name of the Python module to import to get the slots from"
        ' (by default "lhcbnightlyconf"),'
        ' an optional ":name" suffix can be used to specify the attribute '
        "of the module that contains the list of slots to use (by default "
        '"slots")',
    )
    parser.add_argument(
        "--debug",
        action="store_const",
        dest="log_level",
        const=logging.DEBUG,
        help="print debug messages",
    )
    parser.add_argument(
        "--dump-json",
        metavar="FILENAME",
        help="dump all loaded slots configuration as a JSON list of objects",
    )
    parser.set_defaults(module="lhcbnightlyconf", log_level=logging.INFO)
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    slots = loadConfig(args.module)

    print(
        "{0} slots configured ({1} enabled)".format(
            len(slots), len([s for s in list(slots.values()) if s.enabled])
        )
    )

    from tabulate import tabulate

    print(
        tabulate(
            [
                [
                    name,
                    "X" if slots[name].enabled else " ",
                    ", ".join(slots[name].deployment),
                    slots[name]._source,
                ]
                for name in sorted(slots)
            ],
            headers=("slot", "enabled", "deployment", "source"),
            tablefmt="grid",
        ),
        flush=True,
    )

    logging.debug("running semantics checks")
    if not all(check_slot(slot) for slot in slots.values()):
        return 1

    logging.debug("converting slots to JSON")
    json_str = json.dumps([slots[name].toDict() for name in sorted(slots)], indent=2)
    if args.dump_json:
        logging.info("writing slot details to %s", args.dump_json)
        with open(args.dump_json, "w") as f:
            f.write(json_str)

    return 0
