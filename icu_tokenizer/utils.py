# -*- coding: utf-8 -*-

import argparse
import re
import sys
from typing import List

import icu
import regex
from icu import BreakIterator


def apply_break_iterator(
    break_iterator: BreakIterator,
    text: str
) -> List[str]:
    """Apply ICU break iterator on a text."""
    break_iterator.setText(text)
    parts = []
    p0 = 0
    for p1 in break_iterator:
        part = text[p0:p1].strip()
        if len(part) > 0:
            parts.append(part)
        p0 = p1
    return parts


def get_all_unicode_chars():
    """Get all unicode characters."""
    all_unicode_chars = []
    i = 0
    while True:
        try:
            all_unicode_chars.append(chr(i))
        except ValueError:
            break
        i += 1
    return all_unicode_chars


def get_versions() -> dict:
    """Get versions of the various dependecies related to icu_tokenizer."""
    versions = {
        'icu': icu.ICU_VERSION,
        'PyICU': icu.VERSION,
        'regex': regex.__version__
    }

    try:
        import opencc
        versions['opencc'] = opencc.__version__
    except ImportError:
        pass

    return versions


class TextFileType(argparse.FileType):
    """argparse.FileType modified for utf-8 text files."""

    def __init__(self, mode: str = 'r', bufsize: int = -1):
        """TextFileType."""
        self._mode = mode
        self._bufsize = bufsize
        self._encoding = 'utf-8'
        self._errors = 'ignore'

    def __call__(self, string):  # noqa
        # the special argument "-" means sys.std{in,out}
        if string == '-':
            if 'r' in self._mode:
                return sys.stdin
            elif 'w' in self._mode:
                return sys.stdout
            else:
                msg = 'argument "-" with mode {}'.format(self._mode)
                raise ValueError(msg)

        # all other arguments are used as file names
        try:
            return open(string, self._mode, self._bufsize, self._encoding,
                        self._errors)
        except OSError as e:
            msg = "can't open '{}': {}".format(string, e)
            raise argparse.ArgumentTypeError(msg)
