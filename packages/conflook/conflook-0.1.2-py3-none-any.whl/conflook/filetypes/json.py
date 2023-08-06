"""
JSON files
"""

import json
from collections.abc import Sized

from .default import ConfigDoc

TYPE_MAP = {
    "str": "String",
    "list": "Array",
    "dict": "Object",
    "int": "Number",
    "float": "Number",
    "bool": "Boolean",
    "None": "nil",
}


class JSONDoc(ConfigDoc):
    """
    JSON file as dict like config file object.
    """

    def __init__(self, stream=None):
        """
        Create new JSONDoc from a text stream or file.
        """

        if stream is None:
            doc = json.loads("")  # empty
        else:
            doc = json.loads(stream.read())

        super().__init__(doc)

    @staticmethod
    def compatible_suffixes():
        return ["json"]

    @staticmethod
    def get_type_description(obj):
        """
        Return a string which describes the type of the object passed in. It is
        expected that the obj will originate from a JSONDoc.
        """

        desc = obj.__class__.__name__
        desc = TYPE_MAP.get(desc, "UnknownType")
        if isinstance(obj, Sized):
            desc += f"({len(obj)})"
        return desc
