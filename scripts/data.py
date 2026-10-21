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


provinces = get("json/provinces.json")
write("provinces", [[p["code"], p["name_th"], p["name_en"]] for p in provinces])
print(f"GeoThai/data {VERSION}: {len(provinces)} provinces")
