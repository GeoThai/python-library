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


def provinces() -> list[Province]:
    """Lists every province, sorted by code.

    Returns:
        A new list of all 77 provinces.

    Example:
        >>> provinces()[0].name_en
        'Bangkok'
    """
    return list(_provinces())
