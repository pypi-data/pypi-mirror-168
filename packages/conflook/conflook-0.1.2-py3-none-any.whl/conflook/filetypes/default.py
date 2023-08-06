"""
Define abstract config file representation.
"""

import difflib
import functools
import pathlib
from abc import abstractmethod
from collections.abc import Mapping, Sequence, Set, Sized


def is_keychar(char):
    """
    Return True if char is A-Z, a-z, or 0-9.
    """
    if ord(char) >= ord("A") and ord(char) <= ord("Z"):
        return True
    if ord(char) >= ord("a") and ord(char) <= ord("z"):
        return True
    if ord(char) >= ord("0") and ord(char) <= ord("9"):
        return True
    return False


class ConfigDoc(Mapping):
    """
    Abstract config file representation as a nested dictionary like object or list.
    """

    @abstractmethod
    def __init__(self, obj):
        """
        Initalise with a dict/list like obj.
        """
        self._doc = obj  # {} or [] like

    @staticmethod
    @abstractmethod
    def compatible_suffixes():
        """
        Should return a list of strings which are valid file extensions.
        """
        return []

    @staticmethod
    def get_type_description(obj):
        """
        Return a string which describes the type of the object passed in. It is
        expected that the obj will originate from a ConfigDoc.
        """
        desc = obj.__class__.__name__
        if isinstance(obj, Sized):
            desc += f"({len(obj)})"
        return desc

    @classmethod
    def str_of(cls, obj):
        """
        Get string representation of object.
        """
        return str(obj)

    @classmethod
    def has_compatible_suffix(cls, filename):
        """
        Return true if the filename extension is compatable with this handler.
        """
        ext = pathlib.Path(filename).suffix.strip(".").lower()
        return ext in cls.compatible_suffixes()

    def follow_keypath(self, keypath, approx=False):
        """
        Follow the path through nested dicts as described by keypath.

        Keypath is a dot seporated path of keys containing "A-Za-z0-9_-".
        Eg "path.to.2.thing". Not all keys can be addressed in this format.
        If the value is indexable, the number is the index instead of the key.

        If approx is True, follow either
        - the shortest key for which the given key is a prefix
        - a close matching key as determined by difflib

        Returns the value at the end of keypath and the actual keypath followed.
        If the keypath is invalid or can't be followed then return None and a
        string describing the issue.
        """

        keypath = keypath.strip()
        if keypath == "":
            return self._doc, keypath

        keys = keypath.split(".")
        cur = self._doc
        actual_path = []
        for key in keys:
            cur_path = ".".join(actual_path + [key])

            if len(key) == 0 or not all(is_keychar(c) for c in key):
                return None, (
                    "Invalid keypath. Keypath is a dot seporated path "
                    'of keys containing "A-Za-z0-9_-"'
                )

            if all(ord("0") <= ord(c) <= ord("9") for c in key):
                if isinstance(cur, Sequence):
                    if int(key) < len(cur):
                        cur = cur[int(key)]
                    else:
                        return (
                            None,
                            f"Index for '{cur_path}' out of range [{len(cur)}].",
                        )
                else:
                    return None, f"Index for '{cur_path}' must be an integer."

            # Dictionary keys
            elif isinstance(cur, Mapping):
                if key not in cur:
                    if not approx:
                        return None, f"No key '{cur_path}'."

                    fprefix = functools.partial(lambda s, k: s.startswith(k), k=key)
                    prefixs = list(sorted(filter(fprefix, cur.keys())))
                    closest = difflib.get_close_matches(key, cur.keys())
                    if not (prefixs or closest):
                        return None, f"No close matches for {cur_path}'."

                    key = (prefixs or closest)[0]

                cur = cur[key]
            elif isinstance(cur, Set):
                if key not in cur:
                    if not approx:
                        return None, f"No set key '{cur_path}'."

                    fprefix = functools.partial(lambda s, k: s.startswith(k), k=key)
                    prefixs = list(sorted(filter(fprefix, cur)))
                    closest = difflib.get_close_matches(key, cur)
                    if not (prefixs or closest):
                        return None, f"No close matches for {cur_path}'."

                    key = (prefixs or closest)[0]

                cur = key
            else:
                return (
                    None,
                    f"Value at '{cur_path}' is not an explorable mapping or sequence.",
                )

            actual_path.append(key)

        return cur, ".".join(actual_path)

    def __getitem__(self, key):
        if isinstance(self._doc, (Mapping, Sequence)):
            return self._doc[key]
        raise KeyError

    def __iter__(self):
        return iter(self._doc)

    def __len__(self):
        return len(self._doc)

    def __repr__(self):
        return repr(self._doc)
