# ESC-only variant — README

**What this is:** the ESC-only variant of the ASCII/ANSI code
for Unicode and sentential logic. Only the ESC form is the
code here — literal ESC bytes, `ESC[U00ACm` for ¬ (U+00AC),
`ESC[U01F600m` for 😀 (U+1F600). There is no visible `\u`
form in this variant.

Unicode version **18.0.0**, code version **1.1.0**. Full spec:
`../../SPEC.md`. Full test report: `../../TEST_REPORT.md`.
Variant note: `VARIANT.md`. Step-by-step tasks: `HOWTO.md`.
Every logic symbol defined: `SYMBOLS.md`.

## Files in this folder

| File | What it is |
|---|---|
| `README.md` | This file. |
| `HOWTO.md` | Step-by-step tasks. |
| `VARIANT.md` | How this variant differs from the primary Both build. |
| `SYMBOLS.md` | Every logic symbol defined in words. |
| `ascii_unicode_code.py` | The encoder/decoder (same file as the primary build). |

The mapping CSVs are shared and live in the parent folder:
`../../unicode_mapping.csv` (1,114,112 rows) and
`../../logic_mapping.csv` (18 rows). They were not copied
here.

## Run

No installation, no dependencies. Python 3.8 or later
(tested with Python 3.12.3).

```bash
cd ~/workspace/ascii-unicode-code/variants/esc-only
python3 ascii_unicode_code.py --mode esc-only --help
```

## Quick examples

```bash
printf 'Hello, \xe4\xb8\x96\xe7\x95\x8c! \xf0\x9f\x98\x80\n' > /tmp/hello.txt
python3 ascii_unicode_code.py --mode esc-only encode --form esc /tmp/hello.txt | od -c | head
python3 ascii_unicode_code.py --mode esc-only encode --form esc /tmp/hello.txt > /tmp/hello.esc
python3 ascii_unicode_code.py --mode esc-only decode --form esc /tmp/hello.esc
```

`od -c` is used because the output contains real ESC bytes —
a terminal would try to interpret them instead of showing
them. That is expected for this variant.

A logic formula:

```bash
printf '\xc2\xacp \xe2\x88\xa7 q \xe2\x86\x92 r\n' > /tmp/formula.txt
python3 ascii_unicode_code.py --mode esc-only encode --form esc --logic /tmp/formula.txt
```

Expected output: `~p & q -> r` (compact aliases are plain
ASCII, so they are the same in every variant).

## What is an error here, by design

```bash
python3 ascii_unicode_code.py --mode esc-only encode --form visible /tmp/hello.txt
python3 ascii_unicode_code.py --mode esc-only convert --to visible /tmp/hello.esc
```

Both exit with an error: in ESC-only mode there is no
visible form to encode to or convert to. Use `--mode both`
in the primary folder if you want both forms.

## Accessibility and table layout

This documentation follows **ISO/IEC 40500** (WCAG 2.0/2.1,
aim: AA) and **ISO 9241-171** (software accessibility) as
they apply to documentation: every symbol table has
Column 1 = Symbol and Column 2 = Definition in the same
row, with extra columns after the definition; every table
has one header row, no merged cells, and no empty header
cells; nothing is conveyed by colour alone; headings are
used in order; link text is descriptive. The full record
is in `../../README.md`, "Accessibility and table layout".
No HTML version is produced; if one is produced later, its
tables must use `<th scope="col">` and `<th scope="row">`
as appropriate, and must not rely on colour alone.

## Troubleshooting

- **"malformed ESC sequence"** — the input has an ESC byte
  not followed by `[U`, 4 or 6 hex digits, and `m`.
- **"surrogate … is not a valid scalar value"** — surrogates
  (U+D800–U+DFFF) are not characters; fix the input.
- **"non-ASCII byte … in ESC-form input"** — the input file
  contains a byte above 0x7F; it was probably never encoded.
- **Terminal shows nothing / strange colours** — expected:
  use `od -c`, or use the visible-only variant / the primary
  Both build for display.
