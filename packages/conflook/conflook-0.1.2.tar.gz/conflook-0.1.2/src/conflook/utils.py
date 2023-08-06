"""
Utilities.
"""

# https://stackoverflow.com/questions/9778550/which-is-the-correct-way-to-encode-escape-characters-in-python-2-without-killing
# https://docs.python.org/3/library/stdtypes.html

ESCAPE_MAP = dict((k, repr(chr(k))[1:-1]) for k in range(32))
ESCAPE_MAP[0] = "\\0"  # null
ESCAPE_MAP[7] = "\\a"
ESCAPE_MAP[8] = "\\b"
ESCAPE_MAP[11] = "\\v"  # line tabulation
ESCAPE_MAP[12] = "\\f"  # form feed
# ESCAPE_MAP[ord("\\")] = "\\\\"
ESCAPE_MAP[132] = repr(chr(132))[1:-1]  # paragraph seporator
ESCAPE_MAP[133] = repr(chr(133))[1:-1]  # next line
ESCAPE_MAP[8232] = repr(chr(8232))[1:-1]  # line seporator
ESCAPE_MAP[8233] = repr(chr(8233))[1:-1]  # paragraph seporator


def make_printable(string):
    """
    Escape control characters and replace unprintable characters with '?'.
    Not reversable as '\\' not escaped and '?' could be anything.
    """
    return string.translate(ESCAPE_MAP).encode("utf-8", "replace").decode("utf-8")


if __name__ == "__main__":
    INIT = "".join([chr(i) for i in range(2 ** 16)])
    ESC = make_printable(INIT)
    assert " " in ESC
    assert len(ESC.splitlines()) == 1
