import sys
from pathlib import Path

print("STEP 1: imports OK", flush=True)
out = Path(__file__).parent / "test_min.out"
out.write_text("hello", encoding="utf-8")
print(f"STEP 2: wrote {out}", flush=True)
sys.exit(0)
