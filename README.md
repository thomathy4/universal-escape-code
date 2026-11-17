# ASCII/ANSI Code for Unicode and Sentential Logic — README

**What this is:** a code that writes any Unicode text using
ASCII bytes only (0x00–0x7F). Every non-ASCII character and
every control character is replaced by an escape sequence,
and the result can be turned back into the original text
exactly — a round trip.

It was built for Thomas, 2026-11-17, Unicode version **18.0.0**,
code version **1.1.0** (1.0.0 as first built; 1.1.0 adds only the
opt-in abstract surrogate mode). Research only in the sense that no
Notion content was modified to build it; the code itself is
complete and tested (see `TEST_REPORT.md`).

## The two forms (Both — the primary build)

Every character has two interchangeable forms, 1-to-1:

| Form | What it looks like | Example: ¬ (U+00AC) | Example: 😀 (U+1F600) |
|---|---|---|---|
| **ESC form** — the actual code, literal ESC bytes | `ESC [ U` + hex + `m`, where ESC is the byte 0x1B | `ESC[U00ACm` | `ESC[U01F600m` |
| **Visible form** — the same code as printable text | `\uXXXX` (BMP) / `\U00XXXXXX` (astral) | `\u00AC` | `\U0001F600` |

In documents and CSVs the ESC byte is written as the placeholder
`<ESC>`, e.g. `<ESC>[U00ACm`, so the file stays printable. The
real code contains the byte 0x1B — the encoder/decoder work
with the real byte, not the placeholder.

Plain printable ASCII stays as itself. The only exception is
the backslash: in the visible form it is written `\\`, because
a single `\` starts an escape; in the ESC form it stays a
literal backslash.

There are also two single-form variants, built in turn (see
`variants/`): **ESC-only** (`--mode esc-only`) and
**visible-only** (`--mode visible-only`). They use only one
form each. Everything else in this README is about the primary
Both build; the variant folders have their own READMEs.

## Files in this folder

| File | What it is |
|---|---|
| `README.md` | This file. |
| `HOWTO.md` | Step-by-step tasks with copy-paste commands. |
| `SPEC.md` | The full specification. |
| `SYMBOLS.md` | Every logic symbol defined in words. |
| `ascii_unicode_code.py` | The encoder/decoder (Python, stdlib only). |
| `generate_mapping.py` | The script that generated the mapping CSVs. |
| `test_ascii_unicode_code.py` | The test harness. |
| `TEST_REPORT.md` | Test results with exact counts. |
| `UnicodeData.txt` | Source data, Unicode 18.0.0. |
| `unicode_mapping.csv` | One row per code point, 1,114,112 rows, ASCII-only. **On GitHub this file is split** — see the note below. |
| `unicode_mapping_scalars.csv` | One row per scalar value, 1,112,064 rows (surrogates excluded), ASCII-only. **On GitHub this file is split** — see the note below. |
| `mapping/` | The split mapping: 37 chunks under 3 MB each, plus `reassemble.py` and its README. |
| `mapping/scalars/` | The split scalars mapping: chunks under 3 MB each, plus `reassemble.py` and its README. |
| `variants/esc-only/` | ESC-only variant. |
| `variants/visible-only/` | Visible-only variant. |

### Note: the split mapping file (GitHub)

The full `unicode_mapping.csv` is ~105 MB, over GitHub's 100 MB
per-file limit, so on GitHub it is stored as 37 chunks in `mapping/`
(`unicode_mapping.chunk01.csv` … `chunk37.csv`, header in chunk01 only).
To rebuild the original file exactly, from the repository root:

```sh
cat mapping/unicode_mapping.chunk*.csv > unicode_mapping.csv
```

or run `python3 mapping/reassemble.py`, which also checks the SHA-256
(`2c9163c7…84ef`, full value in `mapping/README.md`) and the line count
(1,114,113 including the header). The same file can also be regenerated
with `python3 generate_mapping.py` from `UnicodeData.txt`.

The scalars file, `unicode_mapping_scalars.csv` (~110 MB, 1,112,064
rows + header, surrogates excluded), is split the same way in
`mapping/scalars/` (`unicode_mapping_scalars.chunk01.csv` …,
header in chunk01 only). To rebuild it exactly, from the repository
root:

```sh
cat mapping/scalars/unicode_mapping_scalars.chunk*.csv > unicode_mapping_scalars.csv
```

or run `python3 mapping/scalars/reassemble.py`, which also checks the
SHA-256 (`80f89032…be08a07`, full value in `mapping/scalars/README.md`)
and the line count (1,112,065 including the header).

## Install / run

No installation and no dependencies. You need Python 3.8 or
later (tested with Python 3.12.3).

```bash
cd ~/workspace/universal-escape-code
python3 ascii_unicode_code.py --help
```

That prints the commands: `encode`, `decode`, and `convert`,
each with `--help` of its own, for example:

```bash
python3 ascii_unicode_code.py encode --help
```

## Quick examples

All of these are run from inside `~/workspace/universal-escape-code`.
They are also in `HOWTO.md` with more detail.

### Encode a sentence to the visible form

```bash
printf 'Hello, \xe4\xb8\x96\xe7\x95\x8c! \xf0\x9f\x98\x80\n' > /tmp/hello.txt
python3 ascii_unicode_code.py encode --form visible /tmp/hello.txt
```

Output:

```
Hello, \u4E16\u754C! \U0001F600
```

(The `printf` line writes the UTF-8 bytes for
`Hello, 世界! 😀` followed by a newline. The newline stays
literal — see "Space and new lines" below.)

### Encode the same sentence to the ESC form

```bash
python3 ascii_unicode_code.py encode --form esc /tmp/hello.txt | od -c | head
```

`od -c` is used because the ESC bytes are not printable —
a terminal would try to interpret them instead of showing
them. That is exactly why the visible form exists.

### Decode it back

```bash
python3 ascii_unicode_code.py encode --form visible /tmp/hello.txt > /tmp/hello.vis
python3 ascii_unicode_code.py decode --form visible /tmp/hello.vis
```

Output is the original sentence again.

### Convert ESC form to visible form (and back)

```bash
python3 ascii_unicode_code.py encode --form esc /tmp/hello.txt > /tmp/hello.esc
python3 ascii_unicode_code.py convert --to visible /tmp/hello.esc
python3 ascii_unicode_code.py convert --to esc /tmp/hello.vis
```

Converting is lossless: ESC → visible → ESC gives back the
same bytes.

### Encode a logic formula

```bash
printf '\xc2\xacp \xe2\x88\xa7 q \xe2\x86\x92 r\n' > /tmp/formula.txt
python3 ascii_unicode_code.py encode --form visible /tmp/formula.txt
python3 ascii_unicode_code.py encode --form visible --logic /tmp/formula.txt
```

Output, first command:

```
\u00ACp \u2227 q \u2192 r
```

Output, second command (compact aliases, opt-in):

```
~p & q -> r
```

### Look up a character in the mapping

```bash
grep '^U+00AC,' unicode_mapping.csv
grep '^U+01F600,' unicode_mapping.csv
```

Output:

```
U+00AC,NOT SIGN,172,assigned,<ESC>[U00ACm,\u00AC,~
U+01F600,GRINNING FACE,128512,assigned,<ESC>[U01F600m,\U0001F600,
```

The columns are, in order: codepoint, definition, decimal,
status, ESC form (as `<ESC>…`), visible form, logic alias
(empty unless the character is a logic symbol). Column 1 is
the code point and column 2 is the definition or name,
immediately beside it — see "Accessibility and table layout"
below.

## Space and new lines

- In an encoded stream, a space stays a literal space (0x20).
- A new line (LF) stays a literal LF by default
  (`--preserve-newlines`, which is on). Use
  `--no-preserve-newlines` to encode LF as well.
- A carriage return (CR) is always encoded, so CRLF becomes
  `ESC[U000Dm` + LF (ESC form) or `\u000D` + LF (visible form).
- When a character is being **named** as a code point, it
  always uses its canonical form: space `\u0020`,
  LF `\u000A`, CR `\u000D`. In code:

```bash
python3 -c "from ascii_unicode_code import encode_char; print(encode_char(' ')); print(encode_char(chr(10))); print(encode_char(chr(13)))"
```

## Logic symbols

The 18-symbol inventory is in `logic_mapping.csv` and defined
in words in `SYMBOLS.md`. The core compact aliases are:

| Symbol | Definition | Code point | Compact alias | Long form |
|---|---|---|---|---|
| ¬ | Negation — "not". ¬p is true exactly when p is false. | U+00AC | `~` | `[NOT]` |
| ∧ | Conjunction — "and". | U+2227 | `&` | `[AND]` |
| ∨ | Disjunction — "or" (inclusive). | U+2228 | `\|` | `[OR]` |
| → | Implication — "if … then …". | U+2192 | `->` | `[IF]` |
| ↔ | Biconditional — "if and only if". | U+2194 | `<->` | `[IFF]` |
| ⊃ | Implication (alternative notation), same connective as →. | U+2283 | `=>` | `[IMPLIES]` |
| ≡ | Equivalence — "is equivalent to". | U+2261 | `==` | `[EQUIV]` |
| ⊥ | Falsum — the constant false proposition, always false. | U+22A5 | `_|_` | `[FALSUM]` |
| ⊤ | Verum — the constant true proposition, always true. | U+22A4 | `T` | `[VERUM]` |
| ⊢ | Proves — p can be derived from the premises. | U+22A2 | `\|-` | `[PROVES]` |
| ⊨ | Entails — p is true in every interpretation in which the premises are true. | U+22A8 | `\|=` | `[ENTAILS]` |

The full 18-symbol table, with the remaining seven symbols (∴, ∵, ⊕, ⊻, ↑, ⊬, ⊭), is in `SYMBOLS.md` and in `SPEC.md` §6, in the same layout: Symbol first, Definition second.

Compact aliases are **opt-in** (`--logic` on encode/decode).
Without that flag, `~`, `&`, `|` etc. in text are ordinary
ASCII and are left alone. Note the `T` collision: `T` is both
verum (⊤) and a variable — see `SPEC.md` §6 and `SYMBOLS.md` §9.

## Accessibility and table layout

This documentation follows **ISO/IEC 40500** (the Web Content
Accessibility Guidelines, WCAG 2.0/2.1, aim: AA) and
**ISO 9241-171** (software accessibility) as they apply to
documentation, in these concrete ways:

- **Table layout — definition beside the symbol.** Every
  symbol table in this documentation has Column 1 = Symbol
  and Column 2 = Definition, in the same row, with no other
  column, note, or section separating a symbol from its
  definition. Extra columns (code point, ESC form, visible
  form, alias, long form) come after the definition, never
  before it. The same order is used in the CSVs: in
  `unicode_mapping.csv` column 1 is the code point (the
  symbol itself cannot be shown in an ASCII-only file) and
  column 2 is the definition or name; in `logic_mapping.csv`
  column 1 is the symbol (as its visible form) and column 2
  is the definition in words.
- **Table structure.** Every table has one header row, no
  merged cells, and no empty header cells, so a screen
  reader can announce the column for each cell and the
  tables stay readable when reflowed to a narrow width.
  No table in this documentation relies on colour.
- **No information by colour alone.** Nothing in this
  documentation is conveyed by colour alone — there are no
  colour-coded tables, badges, or status colours. Meaning
  is always in words.
- **Contrast and plain language.** The documentation is
  plain text (Markdown) with no background or foreground
  colours set by the author, so contrast is determined by
  the reader's own viewer and settings. Language is plain
  and direct; technical terms (code point, scalar value,
  surrogate, ESC form) are defined where they are first
  used, in `SPEC.md` §2.
- **Consistent heading structure.** Headings are used in
  order (one top-level heading, then `##`, then `###`),
  with no skipped levels, in `README.md`, `HOWTO.md`,
  `SPEC.md`, and `SYMBOLS.md`, so the document outline is
  navigable by a screen reader.
- **Descriptive link text.** Links in the documentation
  use descriptive text or a full URL that names its
  destination (for example, the UnicodeData.txt source
  URL in `SPEC.md` §1), never "click here".
- **No HTML version is produced.** This documentation is
  Markdown only, so there is no HTML table to mark up.
  If an HTML version is produced later, its tables must
  use `<th scope="col">` for column headers and
  `<th scope="row">` for the symbol cell in each row,
  and must not rely on colour alone — the same rules as
  above, in HTML form.

## Troubleshooting

**"surrogate U+D800 is not a valid scalar value"**
Surrogates (U+D800–U+DFFF) are not characters. The input
contains a lone surrogate — usually from decoding invalid
UTF-8. Fix the input; do not try to encode a surrogate.

Exception, code v1.1.0: the opt-in abstract surrogate mode,
`--abstract-surrogates`, represents a lone surrogate only as the
abstract reference `[SURROGATE U+D800]` (plain ASCII, same in
both forms). Encoding a lone surrogate emits that token;
decoding a surrogate form or the token yields that same token,
never a lone surrogate character. Example:
`printf '\uD800' | python3 ascii_unicode_code.py --mode both decode --form visible --abstract-surrogates`
gives `[SURROGATE U+D800]`. Without the flag, surrogates are
still rejected exactly as above.

**Surrogate pairs are different from lone surrogates, and pair
handling is available.**
A high surrogate followed at once by a low surrogate is how
UTF-16 writes one astral character — the pair is one character
in another spelling, not two characters. For example, the pair
U+D83D U+DE00 is 😀 (U+1F600), and the encoder encodes it as
`\U0001F600`, in both modes, with or without the flag. A lone
surrogate, a low surrogate on its own, or a high surrogate
followed by anything that is not a low surrogate is not a pair:
it is rejected by default, and becomes an abstract token only
with `--abstract-surrogates`.

**"malformed ESC sequence at offset …"**
The ESC-form input has an ESC byte that is not followed by
`[U`, 4 or 6 hex digits, and `m`. Check that the file was
written by this encoder, and that no tool stripped or
replaced the ESC bytes.

**"malformed \u escape at offset …"**
The visible-form input has `\u` not followed by exactly
4 hex digits (or `\U` not followed by exactly 8). Check the
input; `\n` is not a form in this code — LF is `\u000A`.

**"non-ASCII byte … in ESC-form input"**
ESC-form input must be ASCII-only. The file contains a byte
above 0x7F — it is probably a UTF-8 file that was never
encoded, or a visible-form file passed to `--form esc`.

**My terminal shows nothing / strange colours when I print ESC-form output**
That is expected: a terminal interprets ESC sequences.
Use the visible form for display, or pipe ESC-form output
through `od -c` to see the bytes. Never paste ESC-form
output into a document expecting it to display as text.

**`--mode esc-only` / `--mode visible-only` errors**
In ESC-only mode, `--form visible` and `convert --to visible`
are errors by design. In visible-only mode, `--form esc` and
`convert --to esc` are errors by design. Use `--mode both`
(the default) if you want both forms.

## Rebuilding the mapping

```bash
python3 generate_mapping.py
python3 test_ascii_unicode_code.py
```

The generator reads `UnicodeData.txt` in this folder. To use
a newer Unicode version, replace that file, re-run the two
commands above, and update the version number in `SPEC.md`
and in `ascii_unicode_code.py` (`UNICODE_VERSION`).
