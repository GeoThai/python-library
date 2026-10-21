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


@cache
def _provinces() -> tuple[Province, ...]:
    text = files("geothai").joinpath("_data/provinces.json").read_text(encoding="utf-8")
    return tuple(Province(code, name_th, name_en) for code, name_th, name_en in json.loads(text))


@cache
def _province_by_code() -> dict[str, Province]:
    return {p.code: p for p in _provinces()}


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
