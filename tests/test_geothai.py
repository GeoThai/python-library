from geothai import District, Province, districts, province, provinces


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
