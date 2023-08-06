"""
TOML files
"""

import tomlkit

from .default import ConfigDoc


class TOMLDoc(ConfigDoc):
    """
    TOML file as dict like config file object.
    """

    def __init__(self, stream=None):
        """
        Create new TOMLDoc from a text stream or file.
        """

        if stream is None:
            doc = tomlkit.parse("")  # empty
        else:
            doc = tomlkit.parse(stream.read())

        super().__init__(doc)

    @staticmethod
    def compatible_suffixes():
        return ["toml"]
