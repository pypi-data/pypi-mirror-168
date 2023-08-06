"""
YAML files
"""

import io
import re
from collections.abc import Mapping, Sequence, Set, Sized

import yaml
from yaml.constructor import ConstructorError
from yaml.loader import SafeLoader
from yaml.nodes import MappingNode, SequenceNode

from .default import ConfigDoc

TYPE_MAP = {
    "None": "null",
    "dict": "map",
    "list": "seq",
}

PRE = "tag:yaml.org,2002:"  # tag prefix


class YAMLCustomType:
    """Wrapper class for types when want to behave differently."""

    def __init__(self, obj, typename):
        """Wrapper class for custom types."""

        self.obj = obj
        self.typename = typename

    def __str__(self):
        """Wrapper"""
        return str(self.obj)

    def __repr__(self):
        """Wrapper"""
        return repr(self.obj)


class YAMLCustomMapping(YAMLCustomType, Mapping):
    """Behave like a mapping (dict)"""

    def __getitem__(self, k):
        """Wrapper"""
        return self.obj[k]

    def __iter__(self):
        """Wrapper"""
        return iter(self.obj)

    def __len__(self):
        """Wrapper"""
        return len(self.obj)


class YAMLCustomSequence(YAMLCustomType, Sequence):
    """Behave like a sequence (list)"""

    def __getitem__(self, k):
        """Wrapper"""
        return self.obj[k]

    def __len__(self):
        """Wrapper"""
        return len(self.obj)


class YAMLCustomSet(YAMLCustomType, Set, Sequence):
    """Behave like either a set (key only map) and a sequence"""

    def __getitem__(self, k):
        """If key is an integer index as list else index as set"""
        if isinstance(k, int):
            return self.obj[k]
        if k not in self.obj:
            raise KeyError
        return k

    def __iter__(self):
        """Wrapper"""
        return iter(self.obj)

    def __len__(self):
        """Wrapper"""
        return len(self.obj)

    def __str__(self):
        """Display like a set"""
        # replace square brackets with curly brackets
        return "{" + str(self.obj)[1:-1] + "}"

    def __repr__(self):
        """Represent like a set"""
        # replace square brackets with curly brackets
        return "{" + repr(self.obj)[1:-1] + "}"


class YAMLDoc(ConfigDoc):
    """
    YAML file as dict like config file object.
    """

    def __init__(self, stream=None):
        """
        Create new TOMLDoc from a text stream or file.
        """

        # handle custom types
        yaml.add_multi_constructor("", YAMLDoc._multi_constr, Loader=SafeLoader)
        yaml.add_constructor(PRE + "omap", YAMLDoc._omap_constr, Loader=SafeLoader)
        yaml.add_constructor(PRE + "set", YAMLDoc._set_constr, Loader=SafeLoader)
        yaml.add_constructor(PRE + "pairs", YAMLDoc._pairs_constr, Loader=SafeLoader)
        yaml.add_constructor(PRE + "binary", YAMLDoc._binary_constr, Loader=SafeLoader)

        if stream is None:
            doc = yaml.safe_load(io.StringIO(""))  # empty
        else:
            doc = yaml.safe_load(stream)

        super().__init__(doc)

    @staticmethod
    def _multi_constr(loader, tag, node):
        """Generic constructor for unknown types"""
        if isinstance(node, MappingNode):
            return YAMLCustomMapping(loader.construct_mapping(node), tag)
        if isinstance(node, SequenceNode):
            return YAMLCustomSequence(loader.construct_sequence(node), tag)
        return YAMLCustomType(loader.construct_scalar(node), tag)

    @staticmethod
    def _omap_constr(loader, node):
        """Generic constructor for unknown types"""
        omap = list(loader.construct_yaml_omap(node))[0]
        return YAMLCustomMapping(omap, "omap")

    @staticmethod
    def _set_constr(loader, node):
        """constructor for sets"""
        # actually keep in order for display purposes
        # oset = list(loader.construct_yaml_omap(node))[0]
        # return YAMLCustomMapping(oset, "UnorderedSet")
        oset = []
        if not isinstance(node, MappingNode):
            raise ConstructorError(
                "while constructing an ordered map",
                node.start_mark,
                f"expected a sequence, but found {node.id}",
                node.start_mark,
            )

        for nkey, nval in node.value:
            if len(nval.value) != 0:
                raise ConstructorError(
                    "while constructing an ordered map",
                    node.start_mark,
                    f"expected a single mapping item, but found {len(nval.value)} items",
                    nval.start_mark,
                )
            key = loader.construct_object(nkey)
            oset.append(key)
        return YAMLCustomSet(oset, "set")

    @staticmethod
    def _pairs_constr(loader, node):
        """constructor for pairs"""
        return YAMLCustomMapping(list(loader.construct_yaml_pairs(node))[0], "Pairs")

    @staticmethod
    def _binary_constr(loader, node):
        """constructor for binary"""
        binary = loader.construct_scalar(node)
        return YAMLCustomSequence(re.sub(r"\s+", "", binary), "binary")

    @staticmethod
    def compatible_suffixes():
        return ["yaml", "yml"]

    @staticmethod
    def get_type_description(obj):
        if isinstance(obj, YAMLCustomType):
            desc = obj.typename
        else:
            desc = obj.__class__.__name__
            desc = TYPE_MAP.get(desc, desc)

        if isinstance(obj, Sized):
            desc += f"({len(obj)})"
        return desc
