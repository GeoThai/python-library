"""Every province, district, subdistrict and postal code of Thailand."""

import json
from dataclasses import dataclass
from functools import cache
from importlib.resources import files


@dataclass(frozen=True, slots=True)
class Province:
    """A province of Thailand."""

    code: str
    name_th: str
    name_en: str


@dataclass(frozen=True, slots=True)
class District:
    """A district (amphoe or khet) of Thailand."""

    code: str
    name_th: str
    name_en: str
    province_code: str


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
def _districts_by_province() -> dict[str, tuple[District, ...]]:
    grouped: dict[str, list[District]] = {}
    for code, name_th, name_en in _rows("districts"):
        grouped.setdefault(code[:2], []).append(District(code, name_th, name_en, code[:2]))
    return {k: tuple(v) for k, v in grouped.items()}


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
