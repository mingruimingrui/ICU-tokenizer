from typing import List

from icu import BreakIterator, Locale

from icu_tokenizer.utils import apply_break_iterator


class SentSplitter(object):
    """ICU sentence splitter"""

    def __init__(self, lang: str = 'en'):
        self.lang = lang
        self.locale = Locale(lang)
        self.break_iterator = \
            BreakIterator.createSentenceInstance(self.locale)

    def split(self, text: str) -> List[str]:
        return apply_break_iterator(self.break_iterator, text)
