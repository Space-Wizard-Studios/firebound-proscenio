"""Headless round-trip test for the Proscenio writer.

Run via:

    blender --background examples/dummy/dummy.blend --python scripts/test_export.py

Loads the writer directly from blender-addon/ (no extension install needed)
and emits the result to scripts/test_export.out.proscenio.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "blender-addon"))

from exporters.godot import writer  # noqa: E402


def main() -> None:
    # Write beside the atlas so the writer's sibling-atlas heuristic kicks in.
    out = REPO_ROOT / "godot-plugin" / "test_dummy" / "dummy_from_blend.proscenio"
    writer.export(out, pixels_per_unit=100.0)
    print(f"wrote {out}  size={out.stat().st_size}")


if __name__ == "__main__":
    main()
    sys.stdout.flush()
