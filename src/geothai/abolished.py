"""Areas that DOPA abolished. Their codes are no longer in use, but old records may hold them."""

import json
from functools import cache
from importlib.resources import files
from typing import Literal

from geothai import district as district_by_code
from geothai import province as province_by_code
from geothai._areas import is_district, is_province
from geothai._normalize import normalize
from geothai.types import Abolished

__all__ = ["abolished_areas", "match_abolished"]

_LEVELS: dict[int, Literal["province", "district", "subdistrict"]] = {
    2: "province",
    4: "district",
    6: "subdistrict",
}

# code, name_th, name_en, abolished_on, successors, basis, in_force, index into the sources file
_Row = tuple[
    str, str, str | None, str, str, Literal["notice", "name"] | None, str | None, int | None
]


@cache
def _abolished() -> tuple[Abolished, ...]:
    data = files("geothai")
    rows: list[_Row] = json.loads(data.joinpath("_data/abolished.json").read_text(encoding="utf-8"))
    sources: list[str] = json.loads(
        data.joinpath("_data/abolished-sources.json").read_text("utf-8")
    )
    areas: list[Abolished] = []
    for code, name_th, name_en, abolished_on, successors, basis, in_force, source in rows:
        level = _LEVELS.get(len(code))
        if level is None:
            raise ValueError(f"abolished area {code} has no level")
        parent = None if level == "province" else code[:-2]
        areas.append(
            Abolished(
                code=code,
                name_th=name_th,
                name_en=name_en,
                level=level,
                parent_code=parent,
                abolished_on=abolished_on,
                successors=tuple(successors.split(" ")) if successors else (),
                successors_basis=basis,
                successors_in_force=in_force,
                successors_source=None if source is None else sources[source],
            )
        )
    return tuple(areas)


def abolished_areas() -> list[Abolished]:
    """Lists the areas DOPA abolished, sorted by code.

    Returns:
        A new list of abolished districts and subdistricts, with the date each one ended.

    Example:
        >>> next(a for a in abolished_areas() if a.code == "100205").abolished_on
        '2006-01-01'
    """
    return list(_abolished())


def match_abolished(
    subdistrict: str,
    *,
    district: str | None = None,
    province: str | None = None,
) -> list[Abolished]:
    """Finds abolished subdistricts by the name an old record holds.

    Use it when ``geothai.match()`` finds nothing for a name from an old record. A name matches
    after the same clean-up as ``search()``. "เมือง" and "Mueang" mean the capital district
    (code XX01), and "กทม" or "อยุธยา" match their provinces. The current codes are in the
    ``successors`` of each result: pass one to ``geothai.address()`` for the full address.
    Postal codes are not checked, because old records often hold the code of the new area.

    Args:
        subdistrict: The subdistrict name, such as ``"แขวงบางนา"``.
        district: The district name, if the record has one.
        province: The province name, if the record has one.

    Returns:
        Every abolished subdistrict that fits, empty for a name in use today.

    Example:
        >>> found = match_abolished("แขวงบางนา", district="เขตบางนา", province="กทม")
        >>> [(a.code, a.successors) for a in found]
        [('104701', ('104702', '104703'))]
    """
    name = normalize(subdistrict)
    if not name:
        return []
    district_name = normalize(district) if district else ""
    province_name = normalize(province) if province else ""
    found: list[Abolished] = []
    for a in _abolished():
        if a.level != "subdistrict":
            continue
        if name not in (normalize(a.name_th), normalize(a.name_en or "")):
            continue
        p = province_by_code(a.code[:2])
        if province_name and not (p and is_province(p, province_name)):
            continue
        d = district_by_code(a.code[:4])
        if district_name and d and not is_district(d, district_name):
            continue
        found.append(a)
    return found
