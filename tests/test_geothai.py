from geothai import Province, provinces


def test_provinces_lists_all_77_sorted_by_code() -> None:
    found = provinces()
    assert len(found) == 77
    assert found[0] == Province(code="10", name_th="กรุงเทพมหานคร", name_en="Bangkok")
    assert [p.code for p in found] == sorted(p.code for p in found)


def test_provinces_returns_a_new_list_each_call() -> None:
    provinces().pop()
    assert len(provinces()) == 77
