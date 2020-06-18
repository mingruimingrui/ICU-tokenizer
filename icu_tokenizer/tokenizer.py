import re
from typing import List, Union

from icu import BreakIterator, Locale

from icu_tokenizer.url_utils import email_pattern, grubber_url_matcher
from icu_tokenizer.utils import apply_break_iterator

PROTECTED_TEMPLATE = '__PROTECTED_SEQUENCE_{}__'


class Tokenizer(object):
    """ICU based tokenizer with additional functionality to protect sequences.

    Usage:

    >>> tokenizer = Tokenizer(
            lang,
            annotate_hyphens: bool,
            protect_emails_urls: bool,
            extra_protected_patterns: List[Union[str, re.Pattern]] = [],
        )
    >>> tokens: List[str] = tokenizer.tokenize(text)
    """

    HYPHEN_PATTERN = re.compile(r'(\w)\-(?=\w)')
    HYPHEN_PATTERN_REPL = r'\1 @-@ '
    PROTECTED_HYPHEN_PATTERN = re.compile(r'@\-@')

    def __init__(
        self,
        lang: str = 'en',
        annotate_hyphens: bool = False,
        protect_emails_urls: bool = False,
        extra_protected_patterns: List[Union[str, re.Pattern]] = [],
    ):
        """Tokenizer.

        Keyword Arguments:
            lang {str} -- language identifier (default: {'en'})
            annotate_hyphens {bool} -- Protect dashes (default: {False})
            protect_emails_urls {bool} -- Protect urls (default: {False})
            extra_protected_patterns {List[Union[str, re.Pattern]]} --
                A list of regex patterns (default: {[]})
        """
        self.lang = lang
        self.locale = Locale(lang)
        self.break_iterator = \
            BreakIterator.createWordInstance(self.locale)
        self.protected_patterns = []

        self.annotate_hyphens = annotate_hyphens
        if self.annotate_hyphens:
            self.protected_patterns.append(self.PROTECTED_HYPHEN_PATTERN)

        if protect_emails_urls:
            self.protected_patterns.append(email_pattern)
            self.protected_patterns.append(grubber_url_matcher)

        for pattern in extra_protected_patterns:
            if isinstance(pattern, str):
                pattern = re.compile(pattern)
            self.protected_patterns.append(pattern)

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into list of tokens.

        Args:
            text (str): Raw input text.

        Returns:
            List[str]: List of tokens.
        """
        if self.annotate_hyphens:
            text = self.HYPHEN_PATTERN.sub(self.HYPHEN_PATTERN_REPL, text)

        protected_map = {}

        def protect_replace(match):
            protected_str = PROTECTED_TEMPLATE.format(len(protected_map))
            protected_map[protected_str] = match.group(0)
            return ' {} '.format(protected_str)

        for i, pattern in enumerate(self.protected_patterns):
            text = pattern.sub(protect_replace, text)

        tokens = apply_break_iterator(self.break_iterator, text)
        return [protected_map.get(t, t) for t in tokens]
