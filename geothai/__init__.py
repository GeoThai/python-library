import json


from .services.province_service import (
    get_all_provinces,
    get_province_by_code,
    get_provinces_by_criterion,
    Province,
    ProvinceIndex,
    Provinces
)
from .services.district_service import (
    get_all_districts,
    get_district_by_code,
    get_districts_by_criterion,
    District,
    DistrictIndex,
    Districts
)
from .services.subdistrict_service import (
    get_all_subdistricts,
    get_subdistrict_by_code,
    get_subdistricts_by_criterion,
    Subdistrict,
    SubdistrictIndex,
    Subdistricts
)
from .services.postal_code_service import (
    get_all_postal_codes,
    get_postal_codes_by_code,
    PostalCode,
    PostalCodeIndex,
    PostalCodes
)
from .types.metadata_type import Metadata

with open('geothai/data/metadata.json', "r", encoding="utf-8") as f:
    metadata: Metadata = json.load(f)

__all__ = [
    'get_all_provinces',
    'get_province_by_code',
    'get_provinces_by_criterion',
    'Province',
    'ProvinceIndex',
    'Provinces',

    'get_all_districts',
    'get_district_by_code',
    'get_districts_by_criterion',
    'District',
    'DistrictIndex',
    'Districts',

    'get_all_subdistricts',
    'get_subdistrict_by_code',
    'get_subdistricts_by_criterion',
    'Subdistrict',
    'SubdistrictIndex',
    'Subdistricts',

    'get_all_postal_codes',
    'get_postal_codes_by_code',
    'PostalCode',
    'PostalCodeIndex',
    'PostalCodes'
]
