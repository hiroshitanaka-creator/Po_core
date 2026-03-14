#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Project Echo badge SVG")
    parser.add_argument("badge_json", type=Path, help="Path to badge JSON")
    parser.add_argument("--out", type=Path, default=None, help="Output SVG path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    badge = json.loads(args.badge_json.read_text(encoding="utf-8"))
    out = args.out or args.badge_json.with_suffix(".svg")
    from po_echo.badge_svg import write_svg

    write_svg(badge, out)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
