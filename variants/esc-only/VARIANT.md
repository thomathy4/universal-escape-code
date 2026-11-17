# Variant: ESC-only

## How it differs from the primary Both build

The primary build (in `~/workspace/ascii-unicode-code/`) has
**two** interchangeable forms: the ESC form (literal ESC bytes)
and the visible form (`\uXXXX` / `\U00XXXXXX`).

This variant has **only the ESC form**. The visible form is
**not** part of the code in this variant.

- Included: ESC form only — `ESC[U00ACm` for ¬ (U+00AC),
  `ESC[U01F600m` for 😀 (U+1F600). Printable ASCII stays
  literal (backslash is literal 0x5C, no escape). Space and LF
  stay literal in a stream by default, as in the primary build;
  CR is always encoded. Logic compact aliases (`~`, `&`, `|`,
  `->`, …) and long forms work the same way as in the primary
  build, because they are plain ASCII.
- Excluded: the visible form. `\u00AC` is **not** decoded in
  this variant — it is left as the six literal characters
  `\`, `u`, `0`, `0`, `A`, `C`. `convert --to visible` is an
  error. `--form visible` is an error.

## How to use it

The encoder/decoder in this folder is the same file as the
primary build, run with `--mode esc-only`:

```bash
cd ~/workspace/ascii-unicode-code/variants/esc-only
python3 ascii_unicode_code.py --mode esc-only encode --form esc /tmp/hello.txt | od -c | head
python3 ascii_unicode_code.py --mode esc-only decode --form esc /tmp/hello.esc
```

`od -c` is used because the output contains real ESC bytes —
a terminal would try to interpret them instead of showing them.
That is expected behaviour for this variant, and it is why
the visible form exists in the primary build.

The following are errors by design in this variant:

```bash
python3 ascii_unicode_code.py --mode esc-only encode --form visible /tmp/hello.txt
python3 ascii_unicode_code.py --mode esc-only convert --to visible /tmp/hello.esc
```

Both exit with an error naming the mode restriction.

## Mapping files

The mapping CSVs are shared with the primary build and are
**not** copied into this folder, so they are not generated
three times:

- `../../unicode_mapping.csv` — one row per code point,
  1,114,112 rows. The `esc_form` column is the form used by
  this variant (written as `<ESC>[U…m` in the CSV).
- `../../logic_mapping.csv` — the 18-symbol logic inventory.

The `visible_form` column in those CSVs is not part of this
variant's code; it is there because the CSVs are shared with
the Both and visible-only builds.

## Tests for this variant

Run in the primary folder on 2026-11-17, recorded in
`../../TEST_REPORT.md`:

- Spot check: sample round-trip (ASCII, space, ¬, ∧, 😀, a CJK
  character) in `--mode esc-only` — pass 1, fail 0.
- Logic inventory: all 18 symbols round-tripped in
  `--mode esc-only` — pass 18, fail 0.
- Total for this variant in the test harness: **pass 19, fail 0**.
- Negative: ESC-only rejects `--form visible` and
  `convert --to visible` (2 of the 12 negative tests in
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
