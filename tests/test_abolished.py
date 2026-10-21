from geothai import subdistrict
from geothai.abolished import abolished_areas
from geothai.types import Abolished


def test_abolished_areas_lists_every_area_with_its_level_and_parent() -> None:
    found = abolished_areas()
    assert len(found) == 1583
    assert next(a for a in found if a.code == "100205") == Abolished(
        code="100205",
        name_th="บางซื่อ",
        name_en="Bang Sue",
        level="subdistrict",
        parent_code="1002",
        abolished_on="2006-01-01",
    )
    assert len([a for a in found if a.name_en is None]) == 10


def test_no_abolished_code_is_still_an_active_subdistrict() -> None:
    assert [a.code for a in abolished_areas() if subdistrict(a.code)] == []
