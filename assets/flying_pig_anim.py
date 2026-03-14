#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path


def main() -> int:
    out = Path(__file__).with_name("pig_flying.gif")
    try:
        from PIL import Image, ImageDraw

        frames = []
        for i in range(4):
            frame = Image.new("RGB", (220, 120), (20, 30, 60))
            draw = ImageDraw.Draw(frame)
            draw.text((20 + i * 8, 40), "🐷=>", fill=(255, 220, 220))
            frames.append(frame)
        frames[0].save(
            out,
            save_all=True,
            append_images=frames[1:],
            duration=160,
            loop=0,
            format="GIF",
        )
    except Exception:
        # 1x1 transparent GIF fallback
        out.write_bytes(
            b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
        )
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
