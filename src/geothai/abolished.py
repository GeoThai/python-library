"""Areas that DOPA abolished. Their codes are no longer in use, but old records may hold them."""

import json
from functools import cache
from importlib.resources import files
from typing import Literal

from geothai.types import Abolished

__all__ = ["abolished_areas"]

_LEVELS: dict[int, Literal["province", "district", "subdistrict"]] = {
    2: "province",
    4: "district",
    6: "subdistrict",
}


@cache
def _abolished() -> tuple[Abolished, ...]:
    text = files("geothai").joinpath("_data/abolished.json").read_text(encoding="utf-8")
    rows: list[tuple[str, str, str | None, str]] = json.loads(text)
    areas: list[Abolished] = []
    for code, name_th, name_en, abolished_on in rows:
        level = _LEVELS.get(len(code))
        if level is None:
            raise ValueError(f"abolished area {code} has no level")
        parent = None if level == "province" else code[:-2]
        areas.append(Abolished(code, name_th, name_en, level, parent, abolished_on))
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
