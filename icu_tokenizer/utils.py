from typing import List

from icu import BreakIterator


def apply_break_iterator(
    break_iterator: BreakIterator,
    text: str
) -> List[str]:
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
    all_unicode_chars = []
    i = 0
    while True:
        try:
            all_unicode_chars.append(chr(i))
        except ValueError:
            break
        i += 1
    return all_unicode_chars
