"""Generate the goblin placeholder atlas.

Run this once to (re)create `atlas.png`. The generated image is 256x256 with three
80x80 colored regions stacked vertically along the left edge — head (red), torso
(blue), legs (green) — and a magenta debug background everywhere else. The exact
regions match the `texture_region` rectangles inside `goblin.proscenio`.

Requires Pillow. Invoke with the Python that has it installed:

    python examples/goblin/generate_atlas.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ATLAS_SIZE = (256, 256)
DEBUG_BG = (255, 0, 255, 255)  # magenta — anything outside a region is "wrong"

REGIONS: list[tuple[str, tuple[int, int, int, int], tuple[int, int, int, int]]] = [
    # name, (x, y, w, h), rgba fill
    ("head", (0, 0, 80, 80), (220, 70, 70, 255)),
    ("torso", (0, 80, 80, 80), (70, 110, 220, 255)),
    ("legs", (0, 160, 80, 80), (90, 180, 90, 255)),
]


def main() -> None:
    img = Image.new("RGBA", ATLAS_SIZE, DEBUG_BG)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    for name, (x, y, w, h), color in REGIONS:
        draw.rectangle((x, y, x + w - 1, y + h - 1), fill=color, outline=(0, 0, 0, 255))
        if font is not None:
            draw.text((x + 4, y + 4), name, fill=(0, 0, 0, 255), font=font)

    out = Path(__file__).parent / "atlas.png"
    img.save(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
