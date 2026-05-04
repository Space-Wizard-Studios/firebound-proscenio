"""Headless Proscenio test runner.

Invoke from the repository root:

    blender --background examples/goblin/goblin.blend \\
        --python blender-addon/tests/run_tests.py

The script runs inside Blender's bundled Python and has access to `bpy`.
Re-exports the goblin fixture and diffs the result against
`tests/fixtures/goblin/expected.proscenio`. Output is normalized via
`json.dumps(sort_keys=True)` before comparison so dict ordering and
trailing whitespace do not flap.
"""

from __future__ import annotations

import difflib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "blender-addon"))

from exporters.godot import writer  # noqa: E402  — sys.path setup above

EXPECTED = REPO_ROOT / "blender-addon" / "tests" / "fixtures" / "goblin" / "expected.proscenio"


def _normalize(doc: dict) -> str:
    return json.dumps(doc, sort_keys=True, indent=2)


def main() -> int:
    if not EXPECTED.exists():
        print(f"FAIL: missing fixture {EXPECTED}", file=sys.stderr)
        return 1

    out_path = EXPECTED.with_name("actual.proscenio")
    writer.export(out_path, pixels_per_unit=100.0)

    actual = json.loads(out_path.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    actual_s = _normalize(actual)
    expected_s = _normalize(expected)

    if actual_s == expected_s:
        out_path.unlink()
        print("PASS: writer output matches expected fixture")
        return 0

    diff = difflib.unified_diff(
        expected_s.splitlines(),
        actual_s.splitlines(),
        fromfile=EXPECTED.name,
        tofile="actual.proscenio",
        lineterm="",
    )
    print("FAIL: writer output differs from expected fixture", file=sys.stderr)
    for line in diff:
        print(line, file=sys.stderr)
    print(f"\nactual written to: {out_path}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
