import json
from typing import List, Optional, Dict
from typing import TypedDict

from geothai.utils.criteria_matcher import match_criteria


class Province(TypedDict):
    id: int
    province_id: int
    province_name_en: str
    province_name_th: str


with open('geothai/data/provinces.json', 'r', encoding='utf-8') as file:
    provinces_data = json.load(file)

provinces: Dict[int, Province] = {province['province_id']:
                                  province
                                  for province in provinces_data}


def get_all_provinces() -> List[Province]:
    return list(provinces.values())


def get_province_by_id(province_id: int) -> Optional[Province]:
    return provinces.get(province_id)


def get_provinces_by_criterion(criterion: Dict) -> List[Province]:
    return [province
            for province in provinces.values()
            if match_criteria(province, criterion)]
