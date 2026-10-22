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
