from typing import assert_type

from geothai import province
from geothai.types import Province, ProvinceCode, SubdistrictCode


def test_code_types_list_only_real_codes() -> None:
    good: ProvinceCode = "84"
    also_good: SubdistrictCode = "840503"
    bad: ProvinceCode = "99"  # pyright: ignore[reportAssignmentType]
    assert (good, also_good, bad) == ("84", "840503", "99")


def test_fields_keep_their_types() -> None:
    found = province("84")
    assert found is not None
    assert_type(found, Province)
    assert_type(found.name_en, str)
