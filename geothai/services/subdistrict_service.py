import json
from typing import List, Optional, Dict
from typing import TypedDict

from geothai.utils.criteria_matcher import match_criteria


class Subdistrict(TypedDict):
    id: int
    subdistrict_id: int
    district_id: int
    subdistrict_id: int
    subdistrict_name_en: str
    subdistrict_name_th: str
    postal_code: int


with open('geothai/data/subdistricts.json', 'r', encoding='utf-8') as file:
    subdistricts_data = json.load(file)

subdistricts: Dict[int, Subdistrict] = {subdistrict['subdistrict_id']:
                                        subdistrict
                                        for subdistrict in subdistricts_data}


def get_all_subdistricts() -> List[Subdistrict]:
    return list(subdistricts.values())


def get_subdistrict_by_id(subdistrict_id: int) -> Optional[Subdistrict]:
    return subdistricts.get(subdistrict_id)


def get_subdistricts_by_criterion(criterion: Dict) -> List[Subdistrict]:
    return [subdistrict
            for subdistrict in subdistricts.values()
            if match_criteria(subdistrict, criterion)]
