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
import json
import os


def applyenv(envdict, definitions):
    """
    Modify the environment  described by 'envdict' from a list of definitions
    of the type 'name=value', expanding the variables in 'value'.

    >>> env = {}
    >>> applyenv(env, ['foo=bar'])
    >>> env['foo']
    'bar'
    >>> applyenv(env, ['baz=some_${foo}'])
    >>> env['baz']
    'some_bar'

    If a variable in the value is not known, it is replaces with an empty
    string:

    >>> applyenv(env, ['unknown=${var}'])
    >>> env['unknown']
    ''
    """
    from collections import defaultdict
    from string import Template

    # use a temporary dictionary where unkown values default to ''
    tmp = defaultdict(str, envdict)
    # keep track of all explicitly set names
    all_names = set(envdict)
    # apply changes
    for item in definitions:
        name, value = item.split("=", 1)
        all_names.add(name)
        tmp[name] = Template(value).safe_substitute(tmp)
    # copy changes in the input dictionary excluding the variables
    # created as temporary empty placeholders
    envdict.update((k, v) for k, v in list(tmp.items()) if k in all_names)


def sortedByDeps(deps):
    """
    Take a dictionary of dependencies as {'depender': ['dependee', ...]} and
    return the list of keys sorted according to their dependencies so that
    that a key comes after its dependencies.

    When possible the order of insertion in the original dictionary is
    preserved.
    """

    def unique(iterable):
        """Return only the unique elements in the list l.

        >>> unique([0, 0, 1, 2, 1])
        [0, 1, 2]
        """
        uniquelist = []
        for item in iterable:
            if item not in uniquelist:
                uniquelist.append(item)
        return uniquelist

    def recurse(keys):
        """
        Recursive helper function to sort by dependency: for each key we
        first add (recursively) its dependencies then the key itself."""
        result = []
        for k in keys:
            result.extend(recurse(deps[k]))
            result.append(k)
        return unique(result)

    return recurse(deps)


def pushDataToFrontEnd(config_module):
    """
    Sends slots name that can be built to the front-end
    """
    front_end_token = os.environ.get("FRONT_END_TOKEN", None)
    front_end_url = os.environ.get("FRONT_END_URL", None)

    if front_end_url is None:
        raise Exception("Front-end url does not exists in the environment")

    if front_end_token is None:
        raise Exception("Front-end token does not exists in the environment")

    from lb.nightly.configuration import loadConfig

    params = {
        "token": front_end_token,
        "slots": ";".join([name for name in sorted(loadConfig(config_module))]),
    }
    from urllib.parse import urlencode
    from urllib.request import urlopen

    send_data = urlencode(params)
    response = urlopen(front_end_url, send_data)
    response.read()


def save(dest, config):
    """
    Helper function to dump the current configuration to a file.
    """
    f = open(dest, "wb")
    f.write(configToString(config))
    f.close()


def configToString(config):
    """
    Convert the configuration to a string.
    """
    from lb.nightly.configuration import Slot

    if isinstance(config, Slot):
        config = config.toDict()
    return json.dumps(config, sort_keys=True, indent=2, separators=(",", ": "))


def write_patch(patchfile, olddata, newdata, filename):
    """
    Write the difference between olddata and newdata (of filename) in
    patchfile.

    @param patchfile: file object to which write the differences
    @param olddata: old version of the data
    @param newdata: new version of teh data
    @param fileanme: name of the file to be used in the diff headers
    """
    from difflib import context_diff

    if hasattr(olddata, "splitlines"):
        olddata = olddata.splitlines(True)
    if hasattr(newdata, "splitlines"):
        newdata = newdata.splitlines(True)
    for l in context_diff(
        olddata,
        newdata,
        fromfile=os.path.join("a", filename),
        tofile=os.path.join("b", filename),
    ):
        patchfile.write(l)


class _ContainedList(object):
    """
    Helper class to handle a list of projects bound to a slot.
    """

    __type__ = None
    __container_member__ = ""
    __id_member__ = "name"

    def _assertType(self, element):
        """
        Ensure that the type of the parameter is the allowed one.
        """
        types = self.__type__
        if not isinstance(element, types):
            try:
                if len(types) > 1:
                    typenames = ", ".join(t.__name__ for t in types[:-1])
                    typenames += " and " + types[-1].__name__
                elif types:
                    typenames = types[0].__name__
                else:
                    typenames = "()"
            except TypeError:
                typenames = types.__name__
            msg = "only %s instances are allowed (%s was given)" % (
                typenames,
                type(element).__name__,
            )
            raise ValueError(msg)
        return element

    def _assertUnique(self, element, iterable=None):
        """
        Ensure that the there is only one instance of the project.
        """
        for item in iterable or self:
            if element.toDict() == item.toDict():
                raise ValueError(
                    f"There is already project {element} added to the slot."
                )

    def __init__(self, container, iterable=None):
        """
        Initialize the list from an optional iterable, which must contain
        only instances of the required class.
        """
        self.container = container
        if iterable is None:
            self._elements = []
        else:
            self._elements = list(map(self._assertType, iterable))
            for index, element in enumerate(self._elements):
                remainder = [
                    item for idx, item in enumerate(self._elements) if idx != index
                ]
                if remainder:
                    self._assertUnique(element, remainder)
                setattr(element, self.__container_member__, self.container)

    def __eq__(self, other):
        """Equality operator."""
        return (self.__class__ == other.__class__) and (
            self._elements == other._elements
        )

    def __ne__(self, other):
        """Non-equality operator."""
        return not (self == other)

    def __getitem__(self, key):
        """
        Get contained element either by name or by position.
        """
        if isinstance(key, str):
            for element in self._elements:
                id_key = getattr(element, self.__id_member__)
                if key in (id_key, id_key.replace("/", "_")):
                    return element
            raise KeyError("%s %r not found" % (self.__type__.__name__.lower(), key))
        return self._elements[key]

    def __setitem__(self, key, value):
        """
        Item assignment that keeps the binding between container and containee
        in sync.
        """
        if isinstance(key, slice):
            list(map(self._assertType, value))
        else:
            self._assertType(value)
        old = self[key]
        self._elements[key] = value
        if isinstance(key, slice):
            for elem in value:
                setattr(elem, self.__container_member__, self.container)
            for elem in old:
                setattr(elem, self.__container_member__, None)
        else:
            setattr(value, self.__container_member__, self.container)
            setattr(old, self.__container_member__, None)

    def __iter__(self):
        """
        Implement Python iteration protocol.
        """
        for element in self._elements:
            yield element

    def __contains__(self, item):
        """
        Implement Python membership protocol.
        """

        def match(element):
            if item is element:
                return True
            key = getattr(element, self.__id_member__)
            return item == key or item == key.replace("/", "_")

        return any(match(element) for element in self)

    def insert(self, idx, element):
        """
        Item insertion that binds the added object to the container.
        """
        self._assertType(element)
        self._assertUnique(element)
        setattr(element, self.__container_member__, self.container)
        return self._elements.insert(idx, element)

    def append(self, element):
        """
        Item insertion that binds the added object to the container.
        """
        self._assertType(element)
        self._assertUnique(element)
        setattr(element, self.__container_member__, self.container)
        return self._elements.append(element)

    def extend(self, iterable):
        """
        Extend list by appending elements from the iterable.
        """
        for element in iterable:
            self.append(element)

    def __delitem__(self, key):
        """
        Item removal that disconnect the element from the container.
        """
        if isinstance(key, slice):
            old = self[key]
        else:
            old = [self[key]]
        list(map(self.remove, old))

    def remove(self, element):
        """
        Item removal that disconnect the element from the container.
        """
        self._assertType(element)
        self._elements.remove(element)
        setattr(element, self.__container_member__, None)

    def __len__(self):
        """
        Return the number of elements in the list.
        """
        return len(self._elements)
