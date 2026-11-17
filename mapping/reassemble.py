#!/usr/bin/env python3
"""Reassemble unicode_mapping.csv from its split chunks.

The full mapping (1,114,112 rows + header, ~105 MB) exceeds GitHub's
100 MB per-file limit, so it is stored here as 37 plain-text chunks,
each under 3 MB (the GitHub push path rejects ~9 MB requests with
HTTP 413, so chunks are kept under 3 MB):

    mapping/unicode_mapping.chunk01.csv  ...  mapping/unicode_mapping.chunk37.csv

The header row is in chunk01 only. Concatenating the chunks in order
reproduces the original file exactly (SHA-256
2c9163c7c67b8adbab8697c38e580648433d73428c7a23945def5d1826c784ef).

Usage (from the repository root):
    python3 mapping/reassemble.py
    # writes unicode_mapping.csv next to this script's parent, i.e. repo root

Or with the shell:
    cat mapping/unicode_mapping.chunk*.csv > unicode_mapping.csv

The same file can also be regenerated from scratch with:
    python3 generate_mapping.py
(which reads UnicodeData.txt, Unicode 18.0.0).
"""
import hashlib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTS = sorted((pathlib.Path(__file__).resolve().parent).glob("unicode_mapping.chunk*.csv"))
EXPECTED_SHA256 = "2c9163c7c67b8adbab8697c38e580648433d73428c7a23945def5d1826c784ef"
EXPECTED_LINES = 1114113


def main() -> int:
    if not PARTS:
        print("No chunk files found in mapping/.", file=sys.stderr)
        return 1
    out_path = ROOT / "unicode_mapping.csv"
    h = hashlib.sha256()
    lines = 0
    with open(out_path, "wb") as out:
        for part in PARTS:
            with open(part, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
                    out.write(chunk)
            lines += sum(1 for _ in open(part, "rb"))
    print(f"Wrote {out_path} from {len(PARTS)} chunks ({lines} lines).")
    print(f"SHA-256: {h.hexdigest()}")
    if h.hexdigest() != EXPECTED_SHA256:
        print("WARNING: SHA-256 does not match the expected value!", file=sys.stderr)
        return 2
    if lines != EXPECTED_LINES:
        print(f"WARNING: expected {EXPECTED_LINES} lines, got {lines}.", file=sys.stderr)
        return 2
    print("OK: SHA-256 and line count match the original file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
