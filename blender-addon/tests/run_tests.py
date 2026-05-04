"""Headless Proscenio test runner.

Invoke from the repository root:

    blender --background --python blender-addon/tests/run_tests.py

The script runs inside Blender's bundled Python and has access to `bpy`.
"""

from __future__ import annotations

import sys


def main() -> int:
    print("Proscenio test suite — scaffold. Tests land alongside the MVP.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
