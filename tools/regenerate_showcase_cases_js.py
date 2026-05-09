#!/usr/bin/env python3
"""Regenerate the browser-safe data/showcase-cases.js from the CSV."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    csv_path = ROOT / "data" / "showcase-cases.csv"
    js_path = ROOT / "data" / "showcase-cases.js"
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    payload = json.dumps(rows, ensure_ascii=False, indent=2)
    js_path.write_text(f"window.SHOWCASE_CASES = {payload};\n", encoding="utf-8")
    print(f"wrote {len(rows)} rows to {js_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
