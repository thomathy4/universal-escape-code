# ASCII/ANSI Code for Unicode and Sentential Logic — Specification

Version: 1.1.0 of the code (1.0.0 as built 2026-11-17; 1.1.0 adds the
opt-in abstract surrogate mode, `--abstract-surrogates`, only —
no canonical form changed)
Unicode version used: **18.0.0** (UnicodeData.txt downloaded 2026-11-17 from
https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt)
Python used for testing: 3.12.3 (system `unicodedata` is 15.0.0; the mapping
was generated from the downloaded Unicode 18.0.0 data, not from
`unicodedata` — see §9)
Status: built and tested 2026-11-17, as approved by Thomas.

## 1. What this code is

A code that represents any Unicode text using **ASCII bytes only**
(0x00–0x7F). It has two interchangeable forms, 1-to-1 with each other,
plus two single-form variants (see `variants/`):

- **ESC form** — the actual code, with literal ESC bytes.
- **Visible form** — the same code as printable text.

On top of those, an opt-in layer for sentential (propositional) logic:
compact ASCII aliases (`~`, `&`, `|`, `->`, …) and long forms
(`[NOT]`, `[AND]`, …), each mapping 1-to-1 to one canonical form.

Nothing in this code is a secret, a password, or a credential. No
Notion content was modified to build it.

## 2. Definitions

- **Code point**: a number U+0000–U+10FFFF assigned by Unicode.
  There are 1,114,112 of them.
- **Scalar value**: a code point that is not a surrogate
  (U+D800–U+DFFF). There are 1,112,064 scalar values. Only scalar
  values can be characters in text; surrogates are not characters.
- **BMP**: Basic Multilingual Plane, U+0000–U+FFFF.
- **Astral plane**: U+10000–U+10FFFF.
- **ESC**: the ASCII escape byte, 0x1B.
- **ANSI escape sequence**: here, a sequence beginning with ESC,
  in the form `ESC [ … m`, in the style of ANSI SGR sequences.
  This code uses that shape for its ESC form, but the sequence does
  **not** set a colour or a terminal mode — it encodes a character.
  A terminal that displays ESC-form output may try to interpret it;
  that is why the visible form exists.
- **Canonical form**: the ESC form or the visible form of a code
  point, as defined in §3. Every scalar value has exactly one
  canonical ESC form and exactly one canonical visible form.

## 3. The two forms

### 3.1 ESC form

```
ESC '[' 'U' <hex> 'm'
```

- BMP (U+0000–U+FFFF): 4 hex digits, uppercase, zero-padded.
  Example: ¬ (U+00AC) = `ESC[U00ACm`
- Astral (U+10000–U+10FFFF): 6 hex digits, uppercase, zero-padded.
  Example: 😀 (U+1F600) = `ESC[U01F600m`

In this document, and in the CSV files, the ESC byte is written as
the placeholder `<ESC>` so the file stays printable — for example
`<ESC>[U00ACm`. The placeholder is **not** part of the code. The
real code contains the byte 0x1B. The encoder/decoder
(`ascii_unicode_code.py`) works with the real byte.

### 3.2 Visible form

```
\uXXXX        BMP, 4 hex digits
\U00XXXXXX    astral, 8 hex digits (the prefix is \U, then 8 digits)
```

- Example: ¬ (U+00AC) = `\u00AC`
- Example: 😀 (U+1F600) = `\U0001F600`

Hex digits are uppercase in output; the decoder accepts lowercase too.

### 3.3 What stays literal

Printable ASCII, 0x20–0x7E, stays as itself in both forms, with
these exceptions and notes:

| Character | Definition | ESC form | Visible form |
|---|---|---|---|
| Backslash `\` (U+005C) | The backslash character. | literal 0x5C, no escape needed | `\\` (two backslashes) |
| Space (U+0020) | The ordinary word space. | literal 0x20 in a stream (§5) | literal 0x20 in a stream (§5) |
| LF (U+000A) | Line feed, the new-line character. | literal 0x0A if `--preserve-newlines` (default); otherwise encoded | same |
| CR (U+000D) | Carriage return, the return key character. | always encoded in text mode | always encoded in text mode |
| Any other control (U+0000–U+001F except LF, U+007F–U+009F) | A control character other than LF. | encoded | encoded |
| Any non-ASCII character (U+0080 and above) | A character above ASCII. | encoded | encoded |

Why backslash differs: in the visible form a single `\` starts an
escape (`\u`, `\U`, `\\`), so a literal backslash must be doubled
to stay reversible. In the ESC form a backslash is just the byte
0x5C — the ESC byte, not the backslash, is the escape introducer —
so no doubling is needed, and doubling would be wrong.

## 4. Escape rules (decoding)

### 4.1 ESC form decoding

- Scan for ESC. An ESC byte must be followed by `[U`, then 4 or
  6 hex digits, then `m`. Anything else is a **malformed ESC
  sequence** and decoding fails with an error naming the offset.
- 4 digits must name a BMP code point (0x0000–0xFFFF); 6 digits
  must name an astral code point. A value above U+10FFFF is rejected.
- A value in the surrogate range U+D800–U+DFFF is rejected.
- All other bytes must be 0x00–0x7F. A byte above 0x7F in ESC-form
  input is rejected.

### 4.2 Visible form decoding

- `\u` must be followed by exactly 4 hex digits; `\U` by exactly
  8 hex digits. Shorter, longer, or non-hex input is a **malformed
  escape** and decoding fails.
- `\\` decodes to one backslash.
- A backslash followed by any other character is left literal
  (the backslash and the next character are output as-is). In
  particular `\n`, `\r`, `\t` are **not** forms in this code —
  LF is `\u000A` (or a literal LF), CR is `\u000D`.
- A value in the surrogate range, or above U+10FFFF, is rejected.
- Aliases and logic long forms (§6, §7) are decoded only with
  `--aliases`. Without that flag, `[SP]` etc. are left literal.

### 4.3 Conversion ESC ↔ visible

Conversion is lossless and token-by-token: each ESC sequence
becomes the corresponding visible escape, each visible escape
becomes the corresponding ESC sequence, and literal characters
— including a literal LF and a literal space — stay literal.
An encoded LF (`ESC[U000Am` / `\u000A`) stays encoded through
a conversion instead of silently becoming a literal newline,
and a literal LF stays literal. So ESC → visible → ESC is
byte-identical, including for files whose trailing newline
was literal. (An earlier version re-encoded the decoded text
with `preserve_newlines=False`; that changed literal newlines
into encoded ones, and was fixed after the README check
found it — see `TEST_REPORT.md`.)

## 5. Space, LF, CR, CRLF

In an **encoded stream** (ordinary text being encoded):

- Space is the literal byte 0x20.
- LF is the literal byte 0x0A when `--preserve-newlines` is on
  (the default). This keeps line structure visible in the encoded
  file.
- CR is always encoded, so CRLF in the input round-trips as
  `ESC[U000Dm` + LF (ESC form) or `\u000D` + LF (visible form).
- With `--no-preserve-newlines`, LF is encoded too.

When a character is being **named as a code point** (not used as
text), it always uses its canonical form, regardless of the
preserve-newlines setting:

| Character | Definition | Code point | ESC form | Visible form | Alias (visible only) |
|---|---|---|---|---|---|
| Space | The ordinary word space. | U+0020 | `ESC[U0020m` | `\u0020` | `[SP]` |
| Line feed | The new-line character. | U+000A | `ESC[U000Am` | `\u000A` | `[LF]` |
| Carriage return | The return key character. | U+000D | `ESC[U000Dm` | `\u000D` | `[CR]` |
| CRLF (pair) | The pair CR followed by LF, the Windows-style line ending. | U+000D U+000A | `ESC[U000Dm` + LF | `\u000D` + LF | `[CRLF]` |

The function `encode_char(ch)` in the code returns both canonical
forms for one character, always encoded. The aliases `[SP]`,
`[LF]`, `[CR]`, `[CRLF]` exist in the visible form only, are
decoded only with `--aliases`, and are never emitted by the plain
encoder.

## 6. Sentential-logic inventory

See `logic_mapping.csv` and `SYMBOLS.md` for the full defined
inventory (18 symbols). The table below is the core. Every row
maps 1-to-1: one logic symbol ↔ one Unicode code point ↔ one
canonical ESC form ↔ one canonical visible form ↔ at most one
compact alias ↔ one long form.

| Symbol | Definition | Code point | Compact alias | Long form | ESC form | Visible form |
|---|---|---|---|---|---|---|
| ¬ | Negation — "not". ¬p is true exactly when p is false. | U+00AC | `~` | `[NOT]` | `ESC[U00ACm` | `\u00AC` |
| ∧ | Conjunction — "and". p ∧ q is true exactly when both p and q are true. | U+2227 | `&` | `[AND]` | `ESC[U2227m` | `\u2227` |
| ∨ | Disjunction — "or" (inclusive). p ∨ q is true when p, q, or both are true. | U+2228 | `\|` | `[OR]` | `ESC[U2228m` | `\u2228` |
| → | Implication — "if … then …". False only when p is true and q is false. | U+2192 | `->` | `[IF]` | `ESC[U2192m` | `\u2192` |
| ↔ | Biconditional — "if and only if". True exactly when p and q have the same truth value. | U+2194 | `<->` | `[IFF]` | `ESC[U2194m` | `\u2194` |
| ⊃ | Implication (alternative notation) — "if … then …", the same connective as →. | U+2283 | `=>` | `[IMPLIES]` | `ESC[U2283m` | `\u2283` |
| ≡ | Equivalence — "is equivalent to". p and q have the same truth value in every case. | U+2261 | `==` | `[EQUIV]` | `ESC[U2261m` | `\u2261` |
| ⊥ | Falsum — the constant false proposition, always false; also marks a contradiction. | U+22A5 | `_|_` | `[FALSUM]` | `ESC[U22A5m` | `\u22A5` |
| ⊤ | Verum — the constant true proposition, always true. Warning: `T` is also a variable; use it only in formula mode. | U+22A4 | `T` | `[VERUM]` | `ESC[U22A4m` | `\u22A4` |
| ⊢ | Proves — p can be derived (proved) from the premises by the rules of the system. | U+22A2 | `\|-` | `[PROVES]` | `ESC[U22A2m` | `\u22A2` |
| ⊨ | Entails — p is true in every interpretation in which all the premises are true. | U+22A8 | `\|=` | `[ENTAILS]` | `ESC[U22A8m` | `\u22A8` |
| ∴ | Therefore — marks the conclusion of an argument. | U+2234 | `.:.` | `[THEREFORE]` | `ESC[U2234m` | `\u2234` |
| ∵ | Because — marks a reason or premise for a claim. | U+2235 | `:.:` | `[BECAUSE]` | `ESC[U2235m` | `\u2235` |
| ⊕ | Exclusive or (circled-plus form) — true exactly when exactly one of p, q is true. No compact alias: it would collide with ⊻. | U+2295 | — (none) | `[CIRCLED-PLUS]` | `ESC[U2295m` | `\u2295` |
| ⊻ | Exclusive or — true exactly when exactly one of p, q is true. No compact alias: it would collide with ⊕. | U+22BB | — (none) | `[XOR]` | `ESC[U22BBm` | `\u22BB` |
| ↑ | Sheffer stroke (NAND) — "not (p and q)", true except when both p and q are true. No compact alias: `\|` is already disjunction. | U+2191 | — (none) | `[SHEFFER]` | `ESC[U2191m` | `\u2191` |
| ⊬ | Does not prove — p cannot be derived from the premises. No compact alias: it would be ambiguous. | U+22AC | — (none) | `[NOT-PROVES]` | `ESC[U22ACm` | `\u22AC` |
| ⊭ | Does not entail — p is not a semantic consequence of the premises. No compact alias: it would be ambiguous. | U+22AD | — (none) | `[NOT-ENTAILS]` | `ESC[U22ADm` | `\u22AD` |

"— (none)" means **no safe compact alias exists** and none was
invented. Reasons, in brief: ⊕ and ⊻ are both exclusive-or, so a
single `xor` alias would collide; ↑ is the Sheffer stroke (NAND),
but `|` is already disjunction and `^` is not a standard logic
alias here; ⊬ / ⊭ are negated ⊢ / ⊨ and have no standard short
ASCII form that cannot be confused with `|-` / `|=` plus `~`.
Use the long form or the canonical form for those five.

**T collision (⊤).** `T` is both verum (⊤) and a propositional
variable. The compact alias `T` for ⊤ is kept, as approved, but
the decoder maps a bare `T` to ⊤ only in formula mode
(`--logic`), and only when the `T` is not followed by an
alphanumeric character (so `Tom` is not read as ⊤om). Do not use
`--logic` on general text. In general text, use the canonical
form (`ESC[U22A4m` / `\u22A4`) or the long form `[VERUM]`.

**Compact aliases are opt-in.** By default (`--logic` off),
`~`, `&`, `|`, `->` etc. in text are ordinary ASCII and are
left alone. With `--logic` on, encoding replaces each logic
character with its compact alias, and decoding a formula
replaces each compact alias (longest match first: `<->` before
`->`, `_|_` before `|`, etc.) with its logic character.
`--logic` is for formulas only, not for general text.

Long forms are visible-form only and are decoded only with
`--aliases`. They are never emitted by the plain encoder; use
`--logic-long` on encode to emit them.

## 7. Surrogates, noncharacters, private use, unassigned

- **Surrogates** U+D800–U+DFFF: not valid scalar values, not
  characters. A surrogate on its own is rejected with a clear
  error — unless the opt-in abstract surrogate mode is used
  (code v1.1.0, `--abstract-surrogates`). In that mode a lone
  surrogate is represented only as the abstract reference
  `[SURROGATE U+D800]` (plain ASCII, same token in both forms);
  encoding a lone surrogate emits that token, and decoding a
  canonical surrogate form (`ESC[UD800m` / `\uD800`) or the token
  itself yields that same token — never a lone surrogate
  character — so every output stays valid ASCII/UTF-8. The mode
  is off by default. They appear in `unicode_mapping.csv` with status
  `surrogate` and no name, so they are listed, not hidden.
- **Surrogate pairs — the plain difference, and it is available:**
  a pair is not two
  lone surrogates. A high surrogate (U+D800–U+DBFF) followed at
  once by a low surrogate (U+DC00–U+DFFF) is how UTF-16 writes
  one astral character: the pair is one character in another
  spelling, not two characters. Example: the pair U+D83D U+DE00
  is the character 😀 (U+1F600). So the encoder combines a valid
  pair into that astral character and encodes it in the ordinary
  way (`\U0001F600` / `ESC[U01F600m`), and this pair handling is
  available in both modes, with or
  without `--abstract-surrogates`. A lone surrogate, a low
  surrogate on its own, or a high surrogate followed by anything
  that is not a low surrogate is not a pair: it is rejected by
  default, and becomes an abstract token only with
  `--abstract-surrogates`. Decoding does not make pairs:
  decoding `\U0001F600` gives 😀, and decoding two abstract
  tokens gives those two tokens back, because a token is a
  reference to a code point, not a character.
- **Noncharacters** (U+FDD0–U+FDEF and every code point ending
  in FFFE or FFFF, 66 in total): valid scalar values, so they
  round-trip like any other character, but they are permanently
  reserved and have no assigned character. Status `noncharacter`,
  no name.
- **Private use** (U+E000–U+F8FF, U+F0000–U+FFFFD,
  U+100000–U+10FFFD, 137,468 code points): valid scalar values
  with no standard name or meaning. Status `private-use`; the
  UnicodeData name `<Private Use>` is recorded where present.
  No meaning is invented for them.
- **Unassigned** (801,657 code points): no character assigned in
  Unicode 18.0.0. Status `unassigned`, no name. They still have
  a canonical ESC/visible form (the form is defined for every
  code point), and they round-trip as scalar values.
- **Control** (65 code points: U+0000–U+001F, U+007F–U+009F):
  status `control`, name from UnicodeData (e.g. `<control> (LINE
  FEED (LF))`).
- **Assigned** (172,808 code points): status `assigned`, name
  from UnicodeData.txt.

Status counts (total 1,114,112): assigned 172,808; control 65;
private-use 137,468; unassigned 801,657; noncharacter 66;
surrogate 2,048. The generator's "assigned entries" count is
310,341, which is assigned + control + private-use — private-use
ranges are listed in UnicodeData.txt, so they count as entries
there, but they are reported separately as `private-use` in the CSV.

## 8. Files

| File | What it is |
|---|---|
| `SPEC.md` | This specification. |
| `README.md` | Plain-language start-to-finish guide. |
| `HOWTO.md` | Step-by-step tasks. |
| `SYMBOLS.md` | Every logic symbol defined in words. |
| `ascii_unicode_code.py` | Encoder/decoder, stdlib only, CLI. |
| `generate_mapping.py` | Reproducible mapping generator. |
| `test_ascii_unicode_code.py` | Test harness. |
| `TEST_REPORT.md` | Test results with exact counts. |
| `UnicodeData.txt` | Source data, Unicode 18.0.0. |
| `unicode_mapping.csv` | One row per code point, 1,114,112 rows, ASCII-only. |
| `logic_mapping.csv` | Logic inventory, 18 rows, ASCII-only. |
| `variants/esc-only/` | ESC-only variant (see §10). |
| `variants/visible-only/` | Visible-only variant (see §10). |

`unicode_mapping.csv` columns, in order: `codepoint`,
`definition`, `decimal`, `status`, `esc_form`,
`visible_form`, `logic_alias`. Column 1 is the code point
(the symbol itself cannot be shown in an ASCII-only file)
and column 2 is the definition or name, immediately beside
it: assigned and control rows use the Unicode name, and
unassigned, surrogate, noncharacter, and private-use rows
use a status definition (see §7). No row has an empty
definition. `esc_form` in the CSV is the transcription
`<ESC>[U…m` (see §3.1) — the CSV contains **no raw ESC bytes**,
so it stays ASCII-only. `logic_alias` is empty except for the
logic symbols in §6.

`logic_mapping.csv` columns, in order:
`symbol_visible_form`, `definition`, `codepoint`,
`unicode_name`, `esc_form`, `visible_form`, `compact_alias`,
`long_form`. Column 1 is the symbol and column 2 is its
definition in words, immediately beside it. The first column
is the visible-form transcription (e.g. `\u00AC`), not the
raw non-ASCII glyph — a deliberate deviation, so that this
CSV is also ASCII-only. Decode `visible_form` to recover
the glyph.

## 9. Versioning

- Code version: 1.1.0 (1.0.0 as built 2026-11-17; 1.1.0, same day,
  adds only the opt-in abstract surrogate mode).
- Unicode version: 18.0.0, recorded here, in the mapping
  generator, in the encoder (`UNICODE_VERSION = "18.0.0"`), and
  in `TEST_REPORT.md`.
- To rebuild with a newer Unicode version: replace
  `UnicodeData.txt` with the new version's file, re-run
  `python3 generate_mapping.py`, re-run
  `python3 test_ascii_unicode_code.py`, and update the version
  number in this file and in `ascii_unicode_code.py`.
  Do not mix mapping files from different Unicode versions.

## 10. Variants

The primary build is **Both** (ESC + visible, `--mode both`).
Two further variants were built in turn, as Thomas asked:

- **ESC-only** (`variants/esc-only/`, `--mode esc-only`):
  only the ESC form is the code. The encoder emits ESC form
  only; `--form visible` is an error. The decoder accepts ESC
  form only; a visible `\u` sequence is left literal, not
  decoded. `convert --to visible` is an error.
- **Visible-only** (`variants/visible-only/`,
  `--mode visible-only`): only the visible form is the code.
  The encoder emits visible form only; `--form esc` is an
  error. The decoder accepts visible form only; a literal ESC
  byte is an error. `convert --to esc` is an error.

The mapping CSVs are shared — they are identical for all three
variants, so they were not regenerated three times. Each variant
folder has its own `VARIANT.md`, `README.md`, `HOWTO.md`,
`SYMBOLS.md`, and a copy of the encoder run in that mode.
See `variants/esc-only/VARIANT.md` and
`variants/visible-only/VARIANT.md`.

## 11. Worked examples

### 11.1 A logic formula

Input (UTF-8): `¬p ∧ q → r`

- ESC form (default, `--preserve-newlines` on, no `--logic`):
  `ESC[U00ACm` `p` ` ` `ESC[U2227m` ` ` `q` ` ` `ESC[U2192m` ` ` `r`
  (with real ESC bytes; shown here with the `<ESC>` placeholder)
- Visible form: `\u00ACp \u2227 q \u2192 r`
- With `--logic`: `~p & q -> r`

### 11.2 A mixed-language sentence

Input: `Hello, 世界! 😀`

- Visible form: `Hello, \u4E16\u754C! \U0001F600`
- ESC form: `Hello, ` + `ESC[U4E16m` + `ESC[U754Cm` + `! ` +
  `ESC[U01F600m`

### 11.3 Space, LF, CR

Input bytes (UTF-8): `a b` + LF + `c` + CR + LF + `d`

- ESC form, default: `a b` + LF + `c` + `ESC[U000Dm` + LF + `d`
- Named forms: space `[U+0020]` = `ESC[U0020m` / `\u0020`;
  LF = `ESC[U000Am` / `\u000A`; CR = `ESC[U000Dm` / `\u000D`.

## 12. Deviations from the approved design

1. `logic_mapping.csv` first column is `symbol_visible_form`
   (e.g. `\u00AC`) instead of the raw glyph, so the file stays
   ASCII-only. The glyph is recovered by decoding `visible_form`.
2. Conversion is token-by-token (see §4.3), not a
   decode-then-re-encode. An earlier version did
   decode-then-re-encode with `preserve_newlines=False`;
   that silently changed literal newlines into encoded
   ones, so ESC → visible → ESC was not byte-identical.
   The README/HOWTO check found this, and it was fixed
   before delivery.
3. The `∴` / `∵` compact aliases are `.:.` and `:.:` — these
   were not in the approved list (no alias was specified for
   them); they are proposed here, documented as such, and are
   only used with `--logic`. If Thomas prefers no alias for
   them, they can be removed without affecting anything else.
4. `⊕` and `⊻` have no compact alias (see §6); `↑`, `⊬`, `⊭`
   likewise. This follows the approved instruction not to
   invent a colliding alias.
5. Layout change, 2026-11-17 (Thomas): every symbol table
   in this documentation now has Column 1 = Symbol and
   Column 2 = Definition, in the same row, with extra columns
   after the definition. The CSVs were reordered the same
   way (see §8). The `logic_mapping.csv` first column is
   still the visible-form transcription, not the raw glyph,
   so both CSVs stay ASCII-only.

## 13. Accessibility and table layout

This documentation follows **ISO/IEC 40500** (WCAG 2.0/2.1,
aim: AA) and **ISO 9241-171** (software accessibility) as
they apply to documentation. The full record of how is in
`README.md`, "Accessibility and table layout". In short:
every symbol table has Symbol first and Definition second
in the same row; every table has one header row, no merged
cells, and no empty header cells; nothing is conveyed by
colour alone; language is plain; headings are used in order;
link text is descriptive. No HTML version is produced, so
there is no HTML table to mark up; if one is produced
later, its tables must use `<th scope="col">` for column
headers and `<th scope="row">` for the symbol cell in each
row, and must not rely on colour alone.
