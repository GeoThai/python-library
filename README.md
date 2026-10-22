# GeoThai python-library

Every province, district, subdistrict and postal code of Thailand, in one typed Python package with search.

[👉 Website](https://geothai.fasu.dev) · [👉 Data and changelog](https://github.com/GeoThai/data)

## Features

- 77 provinces, 928 districts and 7,436 subdistricts with Thai and English names and DOPA codes
- Postal codes per subdistrict, and a lookup from a postal code to its subdistricts
- Search by Thai or English name, with or without spaces, hyphens or the word for the level
- Frozen dataclasses with a docstring on every field, and `Literal` types for every code
- Data loads on the first call, so `import geothai` stays fast
- No dependencies

## Install

```sh
pip install geothai
```

The package needs Python 3.11 or later.

## Usage

```python
>>> from geothai import address, by_postal_code, districts, province, search, subdistricts
>>> province("84")
Province(code='84', name_th='สุราษฎร์ธานี', name_en='Surat Thani')
>>> len(districts("84"))
19
>>> [s.name_en for s in subdistricts("8405")]
['Ko Pha-ngan', 'Ban Tai', 'Ko Tao']
>>> [s.name_th for s in by_postal_code("84280")]
['เกาะพะงัน', 'บ้านใต้']
>>> a = address("840503")
>>> f"{a.subdistrict.name_th} {a.district.name_th} {a.province.name_th}"
'เกาะเต่า เกาะพะงัน สุราษฎร์ธานี'
>>> [f"{r.level} {r.area.name_th}" for r in search("phangan")]
['district เกาะพะงัน', 'subdistrict เกาะพะงัน']

```

## API

| Function                      | Returns                                                          |
| ----------------------------- | ---------------------------------------------------------------- |
| `provinces()`                 | All 77 provinces, sorted by code                                 |
| `province(code)`              | One province, or `None`                                          |
| `districts(province_code)`    | The districts of a province, empty for an unknown code           |
| `district(code)`              | One district, or `None`                                          |
| `subdistricts(district_code)` | The subdistricts of a district, empty for an unknown code        |
| `subdistrict(code)`           | One subdistrict, or `None`                                       |
| `address(subdistrict_code)`   | The subdistrict with its district and province, or `None`        |
| `by_postal_code(postal_code)` | The subdistricts that use a postal code                          |
| `search(query, *, limit=10)`  | Provinces, districts and subdistricts whose name has the query   |
| `DATA_VERSION`                | The GeoThai/data release in this package, such as `'2026.10.22'` |

Every function takes codes as strings and returns a new list. The areas are frozen dataclasses, so you can use them as dictionary keys.

The areas that DOPA abolished have their own module:

```python
>>> from geothai.abolished import abolished_areas
>>> bang_na = next(a for a in abolished_areas() if a.code == "104701")
>>> bang_na.abolished_on
'2022-04-22'
>>> bang_na.successors
('104702', '104703')
>>> bang_na.successors_basis
'notice'

```

`successors` lists the codes that took an abolished area's place. `successors_basis` says how sure the link is: `"notice"` comes from a Royal Gazette notice, with the date and source in `successors_in_force` and `successors_source`. `"name"` is a match by Thai name for codes DOPA dropped in 2006, likely but not proven. When no successor is known, `successors` is empty.

## Types

```python
from geothai.types import Province, ProvinceCode, SearchResult, Subdistrict
```

| Type                                               | Content                                                       |
| -------------------------------------------------- | ------------------------------------------------------------- |
| `Province`, `District`, `Subdistrict`, `Abolished` | One area. Each field has its description from the data schema |
| `ProvinceCode`, `DistrictCode`, `SubdistrictCode`  | Every code in use, for autocomplete and checks in your editor |
| `Address`, `SearchResult`                          | What `address()` and `search()` return                        |

The functions take `str`, not the code types. A data release can remove a code, and that must not break your type check in a patch update.

## Versions

A new GeoThai/data release ships as a patch version. A change to the API gets a minor or major version. `DATA_VERSION` tells you which data you have. The changes in each data release are at [geothai.fasu.dev/changelog](https://geothai.fasu.dev/changelog/).

## Upgrading from v2

Version 3 is a rewrite on new data. Version 2 did not load its data after install, so code that used it did not run.

| v2                                                    | v3                                      |
| ----------------------------------------------------- | --------------------------------------- |
| `get_all_provinces()`                                 | `provinces()`                           |
| `get_province_by_code(10)`                            | `province("10")`                        |
| `get_all_districts()`, `get_all_subdistricts()`       | `districts(code)`, `subdistricts(code)` |
| `get_district_by_code()`, `get_subdistrict_by_code()` | `district()`, `subdistrict()`           |
| `get_postal_codes_by_code(code)`                      | `by_postal_code(code)`                  |
| `get_provinces_by_criterion(...)` and the others      | A list comprehension on the list        |

The v2 code is on the [`archive`](https://github.com/GeoThai/python-library/tree/archive) branch.

## Why?

Address forms in Thailand need the same four lists, and most copies of them are old: merged postal codes, abolished subdistricts, English names on the wrong area. This package ships the data that GeoThai checks against official sources, with types your editor can read.

## License

The code is [MIT](./LICENSE). The data is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) © 2026 [Pongsakorn Thipayanate](https://github.com/pyyupsk).

If you show the data, credit "GeoThai". Source credits and the license of thailand-geography-json are in [NOTICE](./NOTICE).
