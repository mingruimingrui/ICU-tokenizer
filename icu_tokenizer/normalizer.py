# -*- coding: utf-8 -*-

import re
import unicodedata
from typing import Dict, List

import regex

from icu_tokenizer.utils import get_all_unicode_chars


class Normalizer(object):
    """Performs the follow as part of normalization
    - Ensure NFKC format
    - Handle pseudo-spaces (for numbers)
    - Normalize by unicode category
        https://www.fileformat.info/info/unicode/category/index.htm
        [C*|So|Z*] -> ' '
        [Pc] -> '_'
        [Pd] -> '-'
        [Pf|Pi] -> '"'  # except for apostrophes
        [Ps] -> '('  # except for '{', '['
        [Pe] -> ')'  # except for '}', ']'
    - Normalize Nd (Numbers)
    - Account for some outliers
    - Remove non printable characters
    - Normalize whitespace characters
    - Perform language specific normalization
    """

    def __init__(self, lang='en'):
        # Handle control tokens
        self.ignore_pattern = regex.compile(r'\p{C}|\p{So}|\p{Z}')

        # Handle pseudo-spaces
        # Random note: it appears pseudo-spaces primarily makes a difference
        # when numbers are involved
        self.pseudo_num_pattern = re.compile(r'(\d) (\d)')

        # Punctuation and number replace maps
        self.punct_replace_map = make_punct_replace_map(lang)
        self.punct_pattern = \
            make_pattern_from_keys(self.punct_replace_map.keys())
        self.num_pattern = regex.compile(r'\p{Nd}+')

        # Other language specific normalizers
        self.t2s = None
        if lang == 'zh' or lang.startswith('zh_'):
            try:
                from opencc import OpenCC
            except ImportError:
                raise ImportError('OpenCC library not found')
            self.t2s = OpenCC('t2s')

    def _punct_replace_fn(self, match):
        return self.punct_replace_map[match.group(0)]

    def _num_replace_fn(self, match):
        return str(int(match.group(0)))

    def normalize(self, text):
        text = unicodedata.normalize('NFKC', text)

        text = self.pseudo_num_pattern.sub(r'\1.\2', text)
        text = self.punct_pattern.sub(self._punct_replace_fn, text)
        text = self.num_pattern.sub(self._num_replace_fn, text)

        text = self.ignore_pattern.sub(' ', text)
        text = ' '.join(text.split())  # Normalize whitespace

        if self.t2s is not None:
            text = self.t2s.convert(text)

        return text


def make_pattern_from_keys(keys: List[str]):
    keys = sorted(keys, key=lambda x: len(x), reverse=True)
    pattern_str = r'|'.join(re.escape(k) for k in keys)
    return re.compile(pattern_str)


def make_punct_replace_map(lang: str = 'en') -> Dict[str, str]:
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

    # Consider moving this out of here in the future
    if lang == 'ro':
        # Remove diacritics for romanian
        punct_replace_map['Ş'] = 'S'
        punct_replace_map['ş'] = 's'

        punct_replace_map['Ș'] = 'S'
        punct_replace_map['ș'] = 's'

        punct_replace_map['Ţ'] = 'T'
        punct_replace_map['ţ'] = 't'

        punct_replace_map['Ț'] = 'T'
        punct_replace_map['ț'] = 't'

        punct_replace_map['Ă'] = 'A'
        punct_replace_map['ă'] = 'a'

        punct_replace_map['Â'] = 'A'
        punct_replace_map['â'] = 'a'

        punct_replace_map['Î'] = 'I'
        punct_replace_map['î'] = 'i'

    return punct_replace_map
