import re

# Words people type before a name ("อำเภอ…", "เขต…") and the marks English names differ by.
_PREFIX = re.compile(r"^(?:จังหวัด|อำเภอ|เขต|ตำบล|แขวง|กิ่งอำเภอ)")
_MARKS = re.compile(r"[\s.'-]")
# Short forms need their dot: without it, "อ" is the first letter of names such as อ่างทอง.
_SHORT = re.compile(r"^\s*(?:จ|อ|ต)\.\s*")


def normalize(text: str) -> str:
    """Puts a name or a query in one form so the two can be compared.

    Args:
        text: A Thai or English name, or what a user typed.

    Returns:
        The text in lower case, without spaces, dots, apostrophes, hyphens or a leading
        word for the level. Empty if nothing is left.

    Example:
        >>> normalize("Ko Pha-ngan")
        'kophangan'
        >>> normalize("อำเภอเกาะพะงัน")
        'เกาะพะงัน'
        >>> normalize("อ. เกาะพะงัน")
        'เกาะพะงัน'
    """
    return _PREFIX.sub("", _MARKS.sub("", _SHORT.sub("", text).lower()))
