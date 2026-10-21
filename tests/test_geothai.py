from geothai import (
    District,
    Province,
    Subdistrict,
    district,
    districts,
    province,
    provinces,
    subdistrict,
    subdistricts,
)


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
