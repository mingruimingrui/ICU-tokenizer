from typing import List

from icu import BreakIterator, Locale

from icu_tokenizer.utils import apply_break_iterator


class SentSplitter(object):
    """ICU sentence splitter.

    Usage:

    >>> splitter = SentSplitter(lang)
    >>> sents: List[str] = splitter.split(paragraph)
    """

    def __init__(self, lang: str = 'en'):
        """SentSplitter."""
        self.lang = lang
        self.locale = Locale(lang)
        self.break_iterator = \
            BreakIterator.createSentenceInstance(self.locale)

    def split(self, text: str) -> List[str]:
        """Split a sentence with the ICU sentence splitter."""
        return apply_break_iterator(self.break_iterator, text)
