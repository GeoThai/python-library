"""Every province, district, subdistrict and postal code of Thailand."""

import json
from dataclasses import dataclass
from functools import cache
from importlib.resources import files


@dataclass(frozen=True, slots=True)
class Province:
    code: str
    name_th: str
    name_en: str


@cache
def _provinces() -> tuple[Province, ...]:
    text = files(__package__).joinpath("_data/provinces.json").read_text(encoding="utf-8")
    return tuple(Province(code, name_th, name_en) for code, name_th, name_en in json.loads(text))


def provinces() -> list[Province]:
    """Every province, sorted by code."""
    return list(_provinces())
