import json
from typing import List, Optional

from geothai.utils.criteria_matcher import match_criteria
from geothai.types.district_type import District, DistrictIndex, Districts


with open('geothai/data/districts.json', "r", encoding="utf-8") as f:
    _districts_data: Districts = json.load(f)


def get_all_districts() -> Districts:
    """Return a list of all district records."""
    return list(_districts_data.values())


def get_district_by_code(code: DistrictIndex) -> Optional[District]:
    """Return a single district by its code, or None if not found."""
    return _districts_data.get(code)


def get_districts_by_criterion(criterion: District) -> List[District]:
    """Return a list of districts that match the given criterion."""
    return [d for d in
            _districts_data.values() if match_criteria(d, criterion)]
