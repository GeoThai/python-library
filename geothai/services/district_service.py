import json
from typing import List, Optional, Dict
from typing import TypedDict

from geothai.utils.criteria_matcher import match_criteria


class District(TypedDict):
    id: int
    province_id: int
    district_id: int
    district_name_en: str
    district_name_th: str
    postal_code: int


with open('geothai/data/districts.json', 'r', encoding='utf-8') as file:
    districts_data = json.load(file)

districts: Dict[int, District] = {district['district_id']:
                                  district
                                  for district in districts_data}


def get_all_districts() -> List[District]:
    return list(districts.values())


def get_district_by_id(district_id: int) -> Optional[District]:
    return districts.get(district_id)


def get_districts_by_criterion(criterion: Dict) -> List[District]:
    return [district
            for district in districts.values()
            if match_criteria(district, criterion)]
