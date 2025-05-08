import json
from typing import Optional

from geothai.types.postal_code_type import (
    PostalCode, PostalCodes, PostalCodeIndex
)


with open('geothai/data/postal_codes.json', "r", encoding="utf-8") as f:
    _postal_codes_data: PostalCodes = json.load(f)


def get_all_postal_codes() -> PostalCodes:
    """Return a list of all postal code records."""
    return list(_postal_codes_data.values())


def get_postal_codes_by_code(code: PostalCodeIndex) -> Optional[PostalCode]:
    """Return a single postal code by its code, or None if not found."""
    return _postal_codes_data.get(code)
