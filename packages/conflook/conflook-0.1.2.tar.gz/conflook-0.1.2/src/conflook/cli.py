"""
Entry point to command line interface.
"""

import os
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Sequence

import click

from .filetypes import JSONDoc, TOMLDoc, YAMLDoc
from .utils import make_printable

FILETYPES = [TOMLDoc, JSONDoc, YAMLDoc]


@click.command(
    no_args_is_help=True, help="Show summarised structure or value at keypath."
)
@click.version_option(None, "-v", "--version", package_name="conflook")
@click.help_option("-h", "--help")
# @click.option("--raw", "is_raw", is_flag=True, help="Show full value.")
@click.option(
    "--limit",
    "-l",
    "limit",
    type=click.INT,
    default=10,
    help="Default 10. Truncate output if more than `limit` lines. If 0, there is no limit.",
)
@click.argument("file", type=click.File("rb"))
@click.argument("keypath", default="", required=False)
# pylint: disable=unused-argument
def cli(limit, file, keypath):
    """
    1. Check for valid config file.
    2. Process it into dictonary.
    3. Find value at keypath.
    4. Echo summarised representation of value to terminal.
    """

    if limit <= 0:
        limit = float("inf")

    for cls in FILETYPES:
        if cls.has_compatible_suffix(file.name):
            doc = cls(file)
            break
    else:
        print(f"Unsupported file format '{Path(file.name).suffix}'.", file=sys.stderr)
        supported = []
        for cls in FILETYPES:
            supported.extend(cls.compatible_suffixes())
        print(f"Supported formats: {' '.join(supported)}")
        return

    value, actual_path = doc.follow_keypath(keypath, approx=True)

    if value is None:
        print(actual_path, file=sys.stderr)
        return

    if actual_path:
        print(actual_path + ", ", end="")

    print(doc.get_type_description(value))

    if isinstance(value, Mapping) and not isinstance(value, Sequence):
        its = list(value.items())
        full_size = len(its)
        is_large = (
            full_size - 2 > limit
        )  # -2 prevents truncating if only 1 or 2 need to be
        if is_large:
            its = its[0 : limit // 2] + its[-(limit // 2) :]

        table = []
        for i, (key, val) in enumerate(its):
            str_val = ""
            if hasattr(val, "__str__"):
                # so that str_val is printed on a single line with \n for newlines etc,
                # escape control characters \t \r \n etc and replace unprintible unicode
                # characters with '?'
                str_val = make_printable(doc.str_of(val))

            table.append((key, doc.get_type_description(val), str_val))

        if len(table) > 0:
            ncol1, ncol2, _ = (max(map(len, r)) + 1 for r in zip(*table))
            termwidth, _ = os.get_terminal_size(0)

            for i, (acol, bcol, ccol) in enumerate(table):
                if is_large and i == limit // 2:
                    print(f"... [{full_size - (limit//2)*2}] ...")
                print(acol + " " * (ncol1 - len(acol)), end="")
                print(bcol + " " * (ncol2 - len(bcol)), end="")
                print(ccol[: termwidth - ncol1 - ncol2])
    elif isinstance(value, Sequence) and not isinstance(value, str):
        its = value
        full_size = len(its)
        # -2 prevents truncating if only 1 or 2 need to be
        is_large = full_size - 2 > limit
        if is_large:
            its = its[0 : limit // 2] + its[-(limit // 2) :]
        termwidth, _ = os.get_terminal_size(0)

        for i, val in enumerate(its):
            if is_large and i == limit // 2:
                print(f"... [{full_size - (limit//2)*2}] ...")
            print(make_printable(doc.str_of(val))[:termwidth])
    else:
        print(make_printable(doc.str_of(value))[: termwidth * limit])


if __name__ == "__main__":
    # params filled in by click
    # pylint: disable=no-value-for-parameter
    cli()
