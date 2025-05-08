import json
from typing import List, Optional

from geothai.utils.criteria_matcher import match_criteria
from geothai.types.province_type import Province, ProvinceIndex, Provinces


with open('geothai/data/provinces.json', "r", encoding="utf-8") as f:
    _provinces_data: Provinces = json.load(f)


def get_all_provinces() -> Provinces:
    """Return a list of all province records."""
    return list(_provinces_data.values())


def get_province_by_code(code: ProvinceIndex) -> Optional[Province]:
    """Return a single province by its code, or None if not found."""
    return _provinces_data.get(code)


def get_provinces_by_criterion(criterion: Province) -> List[Province]:
    """Return a list of provinces that match the given criterion."""
    return [d for d in
            _provinces_data.values() if match_criteria(d, criterion)]
