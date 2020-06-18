# -*- coding: utf-8 -*-

import re
import unicodedata
from typing import Dict, List

import regex

from icu_tokenizer.utils import get_all_unicode_chars


class Normalizer(object):
    """Unicode information based normalizer.

    Does the following

    - Ensure NFKC format
    - Handle pseudo-spaces (for numbers)
    - Normalize by unicode categories \
      https://www.fileformat.info/info/unicode/category/index.htm

        - ``[C*|So|Z*]`` → ' '
        - ``[Pc]`` → ``_``
        - ``[Pd]`` → ``-``
        - ``[Pf|Pi]`` → ``"``  (except for ``'``)
        - ``[Ps]`` → ``(``  (except for ``{``, ``[``)
        - ``[Pe]`` → ``)``  (except for ``}``, ``]``)
    - Normalize Nd (Numbers)
    - Account for some outliers
    - Remove non printable characters
    - Normalize whitespace characters
    - Perform language specific normalization

    Usage:

    >>> normalizer = Normalizer(lang, norm_puncts=True)
    >>> norm_text: str = normalizer.normalize(text)
    """

    def __init__(self, lang: str = 'en', norm_puncts: bool = False):
        """Normalizer.

        Args:
            lang (str, optional): Language identifier. Defaults to 'en'.
            norm_puncts (bool, optional): Normalize punctuations?.
                Defaults to False.
        """
        # Handle control tokens
        self.ignore_pattern = regex.compile(r'\p{C}|\p{So}|\p{Z}')

        # Handle pseudo-spaces
        # Random note: it appears pseudo-spaces primarily makes a difference
        # when numbers are involved
        self.pseudo_num_pattern = re.compile(r'(\d) (\d)')

        # Punctuation and number replace maps
        self.num_pattern = regex.compile(r'\p{Nd}+')
        self.punct_replace_map = self.punct_pattern = None
        if norm_puncts:
            self.punct_replace_map = make_punct_replace_map()
            self.punct_pattern = \
                make_pattern_from_keys(self.punct_replace_map.keys())

        # Other language specific normalizers
        lang_replace_map = make_lang_specific_replace_map(lang)
        self.lang_replace_map = self.lang_replace_pattern = None
        if len(lang_replace_map) > 0:
            self.lang_replace_map = lang_replace_map
            self.lang_replace_pattern = \
                make_pattern_from_keys(lang_replace_map.keys())

    def _num_replace_fn(self, match: re.Match) -> str:
        return str(int(match.group(0)))

    def _punct_replace_fn(self, match: re.Match) -> str:
        return self.punct_replace_map[match.group(0)]

    def _lang_replace_fn(self, match: re.Match) -> str:
        return self.lang_replace_map[match.group(0)]

    def normalize(self, text: str) -> str:
        """Perform normalization.

        Args:
            text (str): Input text

        Returns:
            str: Normalized text
        """
        text = unicodedata.normalize('NFKC', text)

        text = self.pseudo_num_pattern.sub(r'\1.\2', text)
        text = self.num_pattern.sub(self._num_replace_fn, text)
        if self.punct_pattern is not None:
            text = self.punct_pattern.sub(self._punct_replace_fn, text)

        text = self.ignore_pattern.sub(' ', text)
        text = ' '.join(text.split())  # Normalize whitespace

        if self.lang_replace_pattern is not None:
            text = self.lang_replace_pattern(self._lang_replace_fn, text)

        return text


def make_pattern_from_keys(keys: List[str]) -> re.Pattern:
    """Make a re.Pattern that matches a list of strings."""
    keys = sorted(keys, key=lambda x: len(x), reverse=True)
    pattern_str = r'|'.join(re.escape(k) for k in keys)
    return re.compile(pattern_str)


def make_punct_replace_map() -> Dict[str, str]:
    """Make the punctuation replace map."""
    # Generate punctuation and number replace maps
    punct_replace_map = {}

    # Normalization rules based on unicode category
    punct_exceptions = {"'", '[', ']', '{', '}'}
    for c in get_all_unicode_chars():
        if c in punct_exceptions:
            continue

        cat = unicodedata.category(c)
        if cat == 'Pc':
            punct_replace_map[c] = '_'
        elif cat == 'Pd':
            punct_replace_map[c] = '-'
        elif cat == 'Pe':
            punct_replace_map[c] = ')'
        elif cat == 'Pf':
            punct_replace_map[c] = '"'
        elif cat == 'Pi':
            punct_replace_map[c] = '"'
        elif cat == 'Ps':
            punct_replace_map[c] = '('

    # User provided rules

    # Soft hyphen
    punct_replace_map['\xad'] = ''

    # Double quotes
    punct_replace_map["''"] = '"'
    punct_replace_map["´´"] = '"'
    punct_replace_map['„'] = '"'

    # Apostrophes
    punct_replace_map["`"] = "'"
    punct_replace_map['´'] = "'"
    punct_replace_map['‘'] = "'"
    punct_replace_map['’'] = "'"
    punct_replace_map['‚'] = "'"  # Not a comma

    # Brackets
    punct_replace_map['【'] = '['
    punct_replace_map['】'] = ']'
    punct_replace_map['［'] = '['
    punct_replace_map['］'] = ']'

    # Common unicode variations
    punct_replace_map['∶'] = ':'
    punct_replace_map['？'] = '?'
    punct_replace_map['．'] = '.'
    punct_replace_map['━'] = '-'
    punct_replace_map['％'] = '%'

    # Chinese punctuations
    punct_replace_map['！'] = '!'
    punct_replace_map['、'] = ','
    punct_replace_map['｜'] = '|'
    punct_replace_map['：'] = ':'
    punct_replace_map['；'] = ';'
    punct_replace_map['，'] = ','
    punct_replace_map['。'] = '.'
    punct_replace_map['～'] = '~'

    # Others
    punct_replace_map['…'] = '...'

    return punct_replace_map


def make_lang_specific_replace_map(lang: str = 'en') -> Dict[str, str]:
    """Create a language specific replace map."""
    replace_map = {}

    if lang == 'ro':
        # Remove diacritics for romanian
        replace_map['Ş'] = 'S'
        replace_map['ş'] = 's'

        replace_map['Ș'] = 'S'
        replace_map['ș'] = 's'

        replace_map['Ţ'] = 'T'
        replace_map['ţ'] = 't'

        replace_map['Ț'] = 'T'
        replace_map['ț'] = 't'

        replace_map['Ă'] = 'A'
        replace_map['ă'] = 'a'

        replace_map['Â'] = 'A'
        replace_map['â'] = 'a'

        replace_map['Î'] = 'I'
        replace_map['î'] = 'i'

    return replace_map
