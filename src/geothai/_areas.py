"""Rules for the names people write for a province or a district."""

from geothai._normalize import normalize
from geothai.types import District, Province

_PROVINCE_ALIASES = {"กทม": "10", "กรุงเทพ": "10", "อยุธยา": "14", "ayutthaya": "14"}


def is_province(p: Province, name: str) -> bool:
    """Tells if a name is this province: its Thai or English name, or a short form people use.

    Args:
        p: The province to compare with.
        name: A name already in ``normalize()`` form.

    Returns:
        ``True`` if the name is this province.
    """
    return (
        name in (normalize(p.name_th), normalize(p.name_en))
        or _PROVINCE_ALIASES.get(name) == p.code
    )


def is_district(d: District, name: str) -> bool:
    """Tells if a name is this district.

    People write the capital district "อ.เมือง" without the province name, so "เมือง" and
    "Mueang" match the capital, which is always the code XX01. Bangkok has no capital district.

    Args:
        d: The district to compare with.
        name: A name already in ``normalize()`` form.

    Returns:
        ``True`` if the name is this district.
    """
    if name in (normalize(d.name_th), normalize(d.name_en)):
        return True
    return d.code.endswith("01") and d.province_code != "10" and name in ("เมือง", "mueang")
