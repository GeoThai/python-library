"""Writes src/geothai/_data/ from the GeoThai/data release named in data.version."""

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "geothai" / "_data"
VERSION = (ROOT / "data.version").read_text(encoding="utf-8").strip()


def get(path: str) -> list[dict[str, str]]:
    url = f"https://raw.githubusercontent.com/GeoThai/data/{VERSION}/{path}"
    with urllib.request.urlopen(url, timeout=60) as res:
        return json.load(res)


def write(name: str, rows: list[list[str]]) -> None:
    text = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    (OUT / f"{name}.json").write_text(text + "\n", encoding="utf-8")


def names(rows: list[dict[str, str]]) -> list[list[str]]:
    return [[r["code"], r["name_th"], r["name_en"]] for r in rows]


provinces = get("json/provinces.json")
districts = get("json/districts.json")
# The package reads each parent from the start of a code, so check that the data agrees.
for d in districts:
    if not d["code"].startswith(d["province_code"]):
        raise ValueError(f"district {d['code']} is not under {d['province_code']}")

write("provinces", names(provinces))
write("districts", names(districts))
print(f"GeoThai/data {VERSION}: {len(provinces)} provinces, {len(districts)} districts")
