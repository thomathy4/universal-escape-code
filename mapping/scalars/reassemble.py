#!/usr/bin/env python3
"""Reassemble unicode_mapping_scalars.csv from its split chunks.

The scalars mapping (1,112,064 rows + header, ~110 MB) exceeds GitHub's
100 MB per-file limit, so it is stored here as 37 plain-text chunks,
each under 3 MB (the GitHub push path rejects ~9 MB requests with
HTTP 413, so chunks are kept under 3 MB):

    mapping/scalars/unicode_mapping_scalars.chunk01.csv  ...  chunk37.csv

The header row is in chunk01 only. Concatenating the chunks in order
reproduces the original file exactly (SHA-256
80f890328a797eecca4f5aa451d793358c21a48ee8eba47eca982d022be08a07).

Usage (from the repository root):
    python3 mapping/scalars/reassemble.py
    # writes unicode_mapping_scalars.csv at the repository root

Or with the shell:
    cat mapping/scalars/unicode_mapping_scalars.chunk*.csv > unicode_mapping_scalars.csv

The scalars file holds one row per scalar value (U+0000–U+10FFFF
except the 2,048 surrogates). It is the same mapping as
unicode_mapping.csv with the surrogate rows removed.
"""
import hashlib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PARTS = sorted((pathlib.Path(__file__).resolve().parent).glob("unicode_mapping_scalars.chunk*.csv"))
EXPECTED_SHA256 = "80f890328a797eecca4f5aa451d793358c21a48ee8eba47eca982d022be08a07"
EXPECTED_LINES = 1112065


def main() -> int:
    if not PARTS:
        print("No chunk files found in mapping/scalars/.", file=sys.stderr)
        return 1
    out_path = ROOT / "unicode_mapping_scalars.csv"
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
