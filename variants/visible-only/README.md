# Visible-only variant — README

**What this is:** the visible-only variant of the ASCII/ANSI
code for Unicode and sentential logic. Only the visible form
is the code here — printable text, `\u00AC` for ¬ (U+00AC),
`\U0001F600` for 😀 (U+1F600). There are no literal ESC bytes
in this variant.

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
cd ~/workspace/ascii-unicode-code/variants/visible-only
python3 ascii_unicode_code.py --mode visible-only --help
```

## Quick examples

```bash
printf 'Hello, \xe4\xb8\x96\xe7\x95\x8c! \xf0\x9f\x98\x80\n' > /tmp/hello.txt
python3 ascii_unicode_code.py --mode visible-only encode --form visible /tmp/hello.txt
python3 ascii_unicode_code.py --mode visible-only encode --form visible /tmp/hello.txt > /tmp/hello.vis
python3 ascii_unicode_code.py --mode visible-only decode --form visible /tmp/hello.vis
```

Expected output of the first command:

```
Hello, \u4E16\u754C! \U0001F600
```

Everything in this variant is printable text, so it can be
displayed, pasted, and printed anywhere ASCII text can.

A logic formula:

```bash
printf '\xc2\xacp \xe2\x88\xa7 q \xe2\x86\x92 r\n' > /tmp/formula.txt
python3 ascii_unicode_code.py --mode visible-only encode --form visible /tmp/formula.txt
python3 ascii_unicode_code.py --mode visible-only encode --form visible --logic /tmp/formula.txt
```

Expected output: `\u00ACp \u2227 q \u2192 r`, then `~p & q -> r`.

## What is an error here, by design

```bash
python3 ascii_unicode_code.py --mode visible-only encode --form esc /tmp/hello.txt
python3 ascii_unicode_code.py --mode visible-only convert --to esc /tmp/hello.vis
```

Both exit with an error: in visible-only mode there is no
ESC form to encode to or convert to. Use `--mode both` in
the primary folder if you want both forms.

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

- **"malformed \u escape"** — `\u` must be followed by
  exactly 4 hex digits (`\U` by exactly 8). `\n` is not a
  form in this code — LF is `\u000A`.
- **"surrogate … is not a valid scalar value"** — surrogates
  (U+D800–U+DFFF) are not characters; fix the input.
- **"literal ESC byte in visible-only input"** — the input
  contains a real ESC byte (0x1B). That is not part of this
  variant; use the ESC-only variant or the primary Both
  build for ESC-form input.
- **A backslash in my text became `\\`** — expected: in the
  visible form a literal backslash is written doubled, so
  decoding can tell it apart from `\u` / `\U`.
