"""Every province, district, subdistrict and postal code of Thailand."""

import json
from functools import cache
from importlib.resources import files

from geothai._normalize import normalize
from geothai.types import Address, District, Province, SearchResult, Subdistrict


def _rows(name: str) -> list[list[str]]:
    text = files("geothai").joinpath(f"_data/{name}.json").read_text(encoding="utf-8")
    return json.loads(text)


@cache
def _provinces() -> tuple[Province, ...]:
    return tuple(Province(code, name_th, name_en) for code, name_th, name_en in _rows("provinces"))


@cache
def _province_by_code() -> dict[str, Province]:
    return {p.code: p for p in _provinces()}


@cache
def _districts() -> tuple[District, ...]:
    return tuple(
        District(code, name_th, name_en, code[:2]) for code, name_th, name_en in _rows("districts")
    )


@cache
def _districts_by_province() -> dict[str, tuple[District, ...]]:
    grouped: dict[str, list[District]] = {}
    for d in _districts():
        grouped.setdefault(d.province_code, []).append(d)
    return {k: tuple(v) for k, v in grouped.items()}


@cache
def _district_by_code() -> dict[str, District]:
    return {d.code: d for d in _districts()}


@cache
def _subdistricts() -> tuple[Subdistrict, ...]:
    return tuple(
        Subdistrict(code, name_th, name_en, code[:4], code[:2], tuple(postal.split(" ")))
        for code, name_th, name_en, postal in _rows("subdistricts")
    )


@cache
def _subdistricts_by_district() -> dict[str, tuple[Subdistrict, ...]]:
    grouped: dict[str, list[Subdistrict]] = {}
    for s in _subdistricts():
        grouped.setdefault(s.district_code, []).append(s)
    return {k: tuple(v) for k, v in grouped.items()}


@cache
def _subdistrict_by_code() -> dict[str, Subdistrict]:
    return {s.code: s for s in _subdistricts()}


@cache
def _subdistricts_by_postal() -> dict[str, tuple[Subdistrict, ...]]:
    grouped: dict[str, list[Subdistrict]] = {}
    for s in _subdistricts():
        for code in s.postal_codes:
            grouped.setdefault(code, []).append(s)
    return {k: tuple(v) for k, v in grouped.items()}


@cache
def _search_index() -> tuple[tuple[SearchResult, tuple[str, str]], ...]:
    results = [
        *(SearchResult("province", p) for p in _provinces()),
        *(SearchResult("district", d) for d in _districts()),
        *(SearchResult("subdistrict", s) for s in _subdistricts()),
    ]
    return tuple((r, (normalize(r.area.name_th), normalize(r.area.name_en))) for r in results)


def provinces() -> list[Province]:
    """Lists every province, sorted by code.

    Returns:
        A new list of all 77 provinces.

    Example:
        >>> provinces()[0].name_en
        'Bangkok'
    """
    return list(_provinces())


def province(code: str) -> Province | None:
    """Finds a province by its code.

    Args:
        code: Two-digit DOPA province code, such as ``"84"``.

    Returns:
        The province, or ``None`` if no province has this code.

    Example:
        >>> province("84").name_en
        'Surat Thani'
        >>> province("99") is None
        True
    """
    return _province_by_code().get(code)


def districts(province_code: str) -> list[District]:
    """Lists the districts of a province, sorted by code.

    Args:
        province_code: Two-digit code of the province.

    Returns:
        A new list, empty if the province code is unknown.

    Example:
        >>> len(districts("84"))
        19
    """
    return list(_districts_by_province().get(province_code, ()))


def district(code: str) -> District | None:
    """Finds a district by its code.

    Args:
        code: Four-digit DOPA district code, such as ``"8405"``.

    Returns:
        The district, or ``None`` if no district has this code.

    Example:
        >>> district("8405").name_th
        'เกาะพะงัน'
    """
    return _district_by_code().get(code)


def subdistricts(district_code: str) -> list[Subdistrict]:
    """Lists the subdistricts of a district, sorted by code.

    Args:
        district_code: Four-digit code of the district.

    Returns:
        A new list, empty if the district code is unknown.

    Example:
        >>> [s.name_en for s in subdistricts("8405")]
        ['Ko Pha-ngan', 'Ban Tai', 'Ko Tao']
    """
    return list(_subdistricts_by_district().get(district_code, ()))


def subdistrict(code: str) -> Subdistrict | None:
    """Finds a subdistrict by its code.

    Args:
        code: Six-digit DOPA subdistrict code, such as ``"840503"``.

    Returns:
        The subdistrict, or ``None`` if no subdistrict has this code.

    Example:
        >>> subdistrict("840503").postal_codes
        ('84360',)
    """
    return _subdistrict_by_code().get(code)


def address(subdistrict_code: str) -> Address | None:
    """Gets a subdistrict with its district and province in one call.

    Args:
        subdistrict_code: Six-digit code of the subdistrict.

    Returns:
        The full address, or ``None`` if the subdistrict code is unknown.

    Example:
        >>> a = address("840503")
        >>> f"{a.subdistrict.name_th} {a.district.name_th} {a.province.name_th}"
        'เกาะเต่า เกาะพะงัน สุราษฎร์ธานี'
    """
    found = _subdistrict_by_code().get(subdistrict_code)
    if found is None:
        return None
    parent_district = _district_by_code().get(found.district_code)
    parent_province = _province_by_code().get(found.province_code)
    if parent_district is None or parent_province is None:
        return None
    return Address(parent_province, parent_district, found)


def by_postal_code(postal_code: str) -> list[Subdistrict]:
    """Finds the subdistricts that use a postal code. One code can cover many subdistricts.

    Args:
        postal_code: Five-digit Thailand Post code, such as ``"84280"``.

    Returns:
        A new list sorted by subdistrict code, empty if no subdistrict uses the code.

    Example:
        >>> [s.name_en for s in by_postal_code("84280")]
        ['Ko Pha-ngan', 'Ban Tai']
    """
    return list(_subdistricts_by_postal().get(postal_code, ()))


def search(query: str, *, limit: int = 10) -> list[SearchResult]:
    """Finds provinces, districts and subdistricts by Thai or English name.

    Case, spaces, hyphens and a leading word such as "อำเภอ" do not matter. Names that start
    with the query come first, then provinces, districts and subdistricts.

    Args:
        query: Part of a name, such as ``"พะงัน"`` or ``"phangan"``.
        limit: Most results to return.

    Returns:
        The matches, empty for an empty query.

    Example:
        >>> [f"{r.level} {r.area.name_th}" for r in search("phangan")]
        ['district เกาะพะงัน', 'subdistrict เกาะพะงัน']
    """
    q = normalize(query)
    if not q:
        return []
    starts: list[SearchResult] = []
    contains: list[SearchResult] = []
    for result, keys in _search_index():
        if any(k.startswith(q) for k in keys):
            starts.append(result)
        elif any(q in k for k in keys):
            contains.append(result)
    return [*starts, *contains][:limit]
