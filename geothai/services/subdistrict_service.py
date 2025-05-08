import json
from typing import List, Optional

from geothai.utils.criteria_matcher import match_criteria
from geothai.types.subdistrict_type import (
    Subdistrict, SubdistrictIndex, Subdistricts
)


with open('geothai/data/subdistricts.json', "r", encoding="utf-8") as f:
    _subdistricts_data: Subdistricts = json.load(f)


def get_all_subdistricts() -> Subdistricts:
    """Return a list of all subdistrict records."""
    return list(_subdistricts_data.values())


def get_subdistrict_by_code(code: SubdistrictIndex) -> Optional[Subdistrict]:
    """Return a single subdistrict by its code, or None if not found."""
    return _subdistricts_data.get(code)


def get_subdistricts_by_criterion(criterion: Subdistrict) -> List[Subdistrict]:
    """Return a list of subdistricts that match the given criterion."""
    return [d for d in
            _subdistricts_data.values() if match_criteria(d, criterion)]
