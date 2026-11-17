# Variant: Visible-only

## How it differs from the primary Both build

The primary build (in `~/workspace/ascii-unicode-code/`) has
**two** interchangeable forms: the ESC form (literal ESC bytes)
and the visible form (`\uXXXX` / `\U00XXXXXX`).

This variant has **only the visible form**. The ESC form is
**not** part of the code in this variant.

- Included: visible form only — `\u00AC` for ¬ (U+00AC),
  `\U0001F600` for 😀 (U+1F600). Printable ASCII stays
  literal, except backslash, which is written `\\`.
  Space and LF stay literal in a stream by default, as in
  the primary build; CR is always encoded. Logic compact
  aliases (`~`, `&`, `|`, `->`, …) and long forms work the
  same way as in the primary build, because they are plain
  ASCII. Readable aliases `[SP]`, `[LF]`, `[CR]`, `[CRLF]`
  are decoded with `--aliases`, as in the primary build.
- Excluded: the ESC form. A literal ESC byte (0x1B) in the
  input is an error, not a code. `convert --to esc` is an
  error. `--form esc` is an error.

## How to use it

The encoder/decoder in this folder is the same file as the
primary build, run with `--mode visible-only`:

```bash
cd ~/workspace/ascii-unicode-code/variants/visible-only
python3 ascii_unicode_code.py --mode visible-only encode --form visible /tmp/hello.txt
python3 ascii_unicode_code.py --mode visible-only decode --form visible /tmp/hello.vis
```

Everything in this variant is printable text, so it can be
displayed, pasted, and printed anywhere ASCII text can.

The following are errors by design in this variant:

```bash
python3 ascii_unicode_code.py --mode visible-only encode --form esc /tmp/hello.txt
python3 ascii_unicode_code.py --mode visible-only convert --to esc /tmp/hello.vis
```

Both exit with an error naming the mode restriction.

## Mapping files

The mapping CSVs are shared with the primary build and are
**not** copied into this folder, so they are not generated
three times:

- `../../unicode_mapping.csv` — one row per code point,
  1,114,112 rows. The `visible_form` column is the form used
  by this variant.
- `../../logic_mapping.csv` — the 18-symbol logic inventory.

The `esc_form` column in those CSVs is not part of this
variant's code; it is there because the CSVs are shared with
the Both and ESC-only builds.

## Tests for this variant

Run in the primary folder on 2026-11-17, recorded in
`../../TEST_REPORT.md`:

- Spot check: sample round-trip (ASCII, space, ¬, ∧, 😀, a CJK
  character) in `--mode visible-only` — pass 1, fail 0.
- Logic inventory: all 18 symbols round-tripped in
  `--mode visible-only` — pass 18, fail 0.
- Total for this variant in the test harness: **pass 19, fail 0**.
- Negative: visible-only rejects `--form esc` and
  `convert --to esc` (2 of the 12 negative tests in
  `TEST_REPORT.md`).

A further sample round-trip was run for this variant report
on 2026-11-17: 5,000 assigned characters (the first 5,000 in
code-point order, which include controls, ASCII, Latin, and
Greek) — **pass 5,000, fail 0**; logic inventory 18/18;
space/LF/CR cases 5/5.

## Documentation in this folder

- `VARIANT.md` — this file.
- `README.md` — plain-language guide for this variant.
- `HOWTO.md` — step-by-step tasks for this variant.
- `SYMBOLS.md` — every logic symbol defined in words
  (same definitions as the primary build).
- `ascii_unicode_code.py` — the encoder/decoder.
- Full spec: `../../SPEC.md`. Full test report:
  `../../TEST_REPORT.md`.
