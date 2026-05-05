"""Headless Proscenio test runner.

Invoke from the repository root:

    blender --background examples/dummy/dummy.blend \\
        --python blender-addon/tests/run_tests.py

The script runs inside Blender's bundled Python and has access to `bpy`.
Re-exports the dummy fixture and diffs the result against
`tests/fixtures/dummy/expected.proscenio`. Output is normalized via
`json.dumps(sort_keys=True)` before comparison so dict ordering and
trailing whitespace do not flap.
"""

from __future__ import annotations

import difflib
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "blender-addon"))

from exporters.godot import writer  # noqa: E402  — sys.path setup above

EXPECTED = REPO_ROOT / "blender-addon" / "tests" / "fixtures" / "dummy" / "expected.proscenio"
SCHEMA = REPO_ROOT / "schemas" / "proscenio.schema.json"


def _normalize(doc: dict[str, Any]) -> str:
    return json.dumps(doc, sort_keys=True, indent=2)


def _validate_against_schema(doc: dict[str, Any]) -> list[str]:
    """Return a list of schema violations for `doc`, empty if valid.

    Falls back gracefully if `jsonschema` is not in Blender's bundled Python
    (it usually is not). Returns an empty list with a stderr note in that
    case so the test still proves the writer round-trip — schema enforcement
    in CI happens in the dedicated `validate-schema` job.
    """
    try:
        import jsonschema  # type: ignore[import-untyped]
    except ImportError:
        print(
            "NOTE: jsonschema not in Blender's Python — skipping in-process "
            "schema validation (CI's validate-schema job covers this).",
            file=sys.stderr,
        )
        return []

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"{'.'.join(str(p) for p in err.absolute_path) or '<root>'}: {err.message}"
        for err in validator.iter_errors(doc)
    ]


def main() -> int:
    if not EXPECTED.exists():
        print(f"FAIL: missing fixture {EXPECTED}", file=sys.stderr)
        return 1

    out_path = EXPECTED.with_name("actual.proscenio")
    writer.export(out_path, pixels_per_unit=100.0)

    actual = json.loads(out_path.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    schema_errors = _validate_against_schema(actual)
    if schema_errors:
        print("FAIL: writer output is not schema-valid", file=sys.stderr)
        for err in schema_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

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
