from typing import TypedDict


class Stats(TypedDict):
    provinces: int
    districts: int
    subdistricts: int
    postal_codes: int


class Metadata(TypedDict):
    version: str
    last_updated: str
    source: str
    stats: Stats
