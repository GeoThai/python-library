"""Types of the areas and results that ``geothai`` returns."""

from dataclasses import dataclass
from typing import Literal

from geothai._schema import (
    District,
    DistrictCode,
    Province,
    ProvinceCode,
    Subdistrict,
    SubdistrictCode,
)

__all__ = [
    "Address",
    "District",
    "DistrictCode",
    "Province",
    "ProvinceCode",
    "SearchResult",
    "Subdistrict",
    "SubdistrictCode",
]


@dataclass(frozen=True, slots=True)
class Address:
    """A subdistrict together with the district and province it is in."""

    province: Province
    district: District
    subdistrict: Subdistrict


@dataclass(frozen=True, slots=True)
class SearchResult:
    """One match from ``search()``. Check ``level`` to know which kind of area ``area`` is."""

    level: Literal["province", "district", "subdistrict"]
    area: Province | District | Subdistrict
