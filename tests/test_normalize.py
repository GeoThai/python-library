import pytest

from geothai._normalize import normalize


def test_normalize_drops_case_spaces_and_marks() -> None:
    assert normalize("Ko Pha-ngan") == "kophangan"
    assert normalize("Ban Na'ng. Rong") == "bannangrong"


@pytest.mark.parametrize("word", ["จังหวัด", "อำเภอ", "เขต", "ตำบล", "แขวง", "กิ่งอำเภอ"])
def test_normalize_drops_a_leading_word_for_the_level(word: str) -> None:
    assert normalize(f"{word}พระนคร") == "พระนคร"


def test_normalize_keeps_the_word_inside_a_name() -> None:
    assert normalize("บางเขต") == "บางเขต"


def test_normalize_leaves_nothing_for_blank_text() -> None:
    assert normalize("  - ") == ""


def test_normalize_drops_a_short_form_only_with_its_dot() -> None:
    assert normalize("จ.สุราษฎร์ธานี") == "สุราษฎร์ธานี"
    assert normalize(" อ. เกาะพะงัน") == "เกาะพะงัน"
    assert normalize("ต.เกาะเต่า") == "เกาะเต่า"
    assert normalize("อ่างทอง") == "อ่างทอง"
    assert normalize("ตราด") == "ตราด"
