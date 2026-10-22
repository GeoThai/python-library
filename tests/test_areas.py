from geothai import district, province
from geothai._areas import is_district, is_province
from geothai._normalize import normalize


def test_is_province_reads_full_names_and_short_forms() -> None:
    bangkok, ayutthaya = province("10"), province("14")
    assert bangkok is not None
    assert ayutthaya is not None
    for name in ("จ.กรุงเทพมหานคร", "Bangkok", "กทม", "กรุงเทพ"):
        assert is_province(bangkok, normalize(name))
    assert is_province(ayutthaya, normalize("อยุธยา"))
    assert not is_province(bangkok, normalize("อยุธยา"))


def test_is_district_reads_the_capital_district_except_in_bangkok() -> None:
    mueang, bang_rak = district("8401"), district("1004")
    assert mueang is not None
    assert bang_rak is not None
    for name in ("อ.เมือง", "Mueang", "เมืองสุราษฎร์ธานี"):
        assert is_district(mueang, normalize(name))
    assert not is_district(bang_rak, normalize("เมือง"))
