import pytest

from geothai import (
    address,
    by_postal_code,
    district,
    districts,
    province,
    provinces,
    search,
    subdistrict,
    subdistricts,
)
from geothai.types import District, Province, Subdistrict


def test_provinces_lists_all_77_sorted_by_code() -> None:
    found = provinces()
    assert len(found) == 77
    assert found[0] == Province(code="10", name_th="กรุงเทพมหานคร", name_en="Bangkok")
    assert [p.code for p in found] == sorted(p.code for p in found)


def test_provinces_returns_a_new_list_each_call() -> None:
    provinces().pop()
    assert len(provinces()) == 77


def test_province_finds_one_by_code() -> None:
    assert province("84") == Province(code="84", name_th="สุราษฎร์ธานี", name_en="Surat Thani")
    assert province("99") is None


def test_districts_lists_the_districts_of_a_province() -> None:
    found = districts("84")
    assert len(found) == 19
    assert found[4] == District(
        code="8405", name_th="เกาะพะงัน", name_en="Ko Pha-ngan", province_code="84"
    )
    assert districts("99") == []


def test_every_province_has_districts_928_in_all() -> None:
    assert sum(len(districts(p.code)) for p in provinces()) == 928


def test_district_finds_one_by_code() -> None:
    assert district("1001") == District(
        code="1001", name_th="เขตพระนคร", name_en="Phra Nakhon", province_code="10"
    )
    assert district("84") is None
    assert district("9999") is None


def test_subdistricts_lists_the_subdistricts_of_a_district() -> None:
    found = subdistricts("8405")
    assert [s.code for s in found] == ["840501", "840502", "840503"]
    assert found[0] == Subdistrict(
        code="840501",
        name_th="เกาะพะงัน",
        name_en="Ko Pha-ngan",
        district_code="8405",
        province_code="84",
        postal_codes=("84280",),
    )
    assert subdistricts("9999") == []


def test_every_district_has_subdistricts_7436_in_all() -> None:
    every = [s for p in provinces() for d in districts(p.code) for s in subdistricts(d.code)]
    assert len(every) == 7436


def test_subdistrict_finds_one_by_code() -> None:
    found = subdistrict("840503")
    assert found is not None
    assert found.name_en == "Ko Tao"
    hua_mak = subdistrict("100608")
    assert hua_mak is not None
    assert hua_mak.postal_codes == ("10240", "10250")
    assert subdistrict("8405") is None
    assert subdistrict("999999") is None


def test_address_gives_the_full_chain_of_a_subdistrict() -> None:
    found = address("840503")
    assert found is not None
    assert found.subdistrict.name_en == "Ko Tao"
    assert found.district.name_en == "Ko Pha-ngan"
    assert found.province.name_en == "Surat Thani"
    assert address("8405") is None


def test_every_subdistrict_has_a_full_address() -> None:
    codes = [s.code for p in provinces() for d in districts(p.code) for s in subdistricts(d.code)]
    assert all(address(code) for code in codes)


def test_by_postal_code_finds_every_subdistrict_that_uses_a_code() -> None:
    assert [s.code for s in by_postal_code("84280")] == ["840501", "840502"]
    assert "100608" in [s.code for s in by_postal_code("10250")]
    assert by_postal_code("00000") == []


def found(query: str, limit: int = 10) -> list[str]:
    return [f"{r.level} {r.area.code}" for r in search(query, limit=limit)]


@pytest.mark.parametrize("query", ["พะงัน", "phangan", "Pha-ngan", "pha ngan"])
def test_search_finds_a_name_in_thai_or_english(query: str) -> None:
    assert found(query) == ["district 8405", "subdistrict 840501"]


def test_search_puts_names_that_start_with_the_query_first_then_by_level() -> None:
    assert found("สุราษฎร์", 3) == ["province 84", "district 8401", "subdistrict 700403"]


def test_search_ignores_the_word_for_the_level() -> None:
    assert found("อำเภอเกาะพะงัน") == found("เกาะพะงัน")
    assert "district 1001" in found("เขตพระนคร")


def test_search_returns_nothing_for_an_empty_query_and_respects_the_limit() -> None:
    assert search("  ") == []
    assert len(search("a", limit=5)) == 5
