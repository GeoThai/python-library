from geothai import district, subdistrict
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
        successors=("102901",),
        successors_basis="name",
        successors_in_force=None,
        successors_source=None,
    )
    assert len([a for a in found if a.name_en is None]) == 10


def test_no_abolished_code_is_still_an_active_subdistrict() -> None:
    assert [a.code for a in abolished_areas() if subdistrict(a.code)] == []


def test_abolished_areas_carry_their_successors_and_the_notice_behind_them() -> None:
    found = abolished_areas()
    bang_na = next(a for a in found if a.code == "104701")
    assert bang_na.successors == ("104702", "104703")
    assert bang_na.successors_basis == "notice"
    assert bang_na.successors_in_force == "2017-07-26"
    assert "ราชกิจจานุเบกษา เล่ม 134" in (bang_na.successors_source or "")
    with_successors = [a for a in found if a.successors]
    assert len(with_successors) == 1182
    codes = [c for a in with_successors for c in a.successors or ()]
    assert [c for c in codes if not (district(c) if len(c) == 4 else subdistrict(c))] == []
