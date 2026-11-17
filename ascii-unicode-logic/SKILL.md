---
name: ascii-unicode-logic
description: Encode and decode sentential-logic formulas and Unicode text between ASCII/ANSI ESC form ESC[U00ACm and visible form \u00AC. Use when the user asks to encode, decode, convert, or check logic symbols or any Unicode character, or says "use the logic code".
license: MIT
compatibility: Python 3.10+ stdlib only; no network, no pip install.
---

# ASCII/Unicode Logic Code

Unicode 18.0.0, code v1.1.0. Source: `SPEC.md` in `references/`.
Full mapping of all 1,114,112 code points is NOT in this folder — see
"Do not upload the full mapping" below.

## When to use

- User asks to encode, decode, or convert a formula or text, or to check a symbol.
- User says "use the logic code".
- Always prefer the script over guessing a code point.

## The two forms (never invent a code point)

| Symbol | Definition | Code point | ESC form | Visible form |
|---|---|---|---|---|
| ¬ | Negation — "not". ¬p is true exactly when p is false. | U+00AC | `ESC[U00ACm` | `\u00AC` |
| ∧ | Conjunction — "and". p ∧ q is true exactly when both p and q are true. | U+2227 | `ESC[U2227m` | `\u2227` |
| ∨ | Disjunction — "or" (inclusive). p ∨ q is true when p is true, or q is true, or both are true. | U+2228 | `ESC[U2228m` | `\u2228` |
| → | Implication — "if … then …". p → q is false only when p is true and q is false. | U+2192 | `ESC[U2192m` | `\u2192` |
| ↔ | Biconditional — "if and only if". p ↔ q is true exactly when p and q have the same truth value. | U+2194 | `ESC[U2194m` | `\u2194` |
| ⊃ | Implication (alternative notation) — same connective as →, in the older notation. | U+2283 | `ESC[U2283m` | `\u2283` |
| ≡ | Equivalence — "is equivalent to". p ≡ q have the same truth value in every case. | U+2261 | `ESC[U2261m` | `\u2261` |
| ⊥ | Falsum — the constant false proposition, always false; also marks a contradiction. | U+22A5 | `ESC[U22A5m` | `\u22A5` |
| ⊤ | Verum — the constant true proposition, always true. Warning: `T` is also a propositional variable, so use the `T` alias only in formula mode (`--logic`); in general text use the canonical form or `[VERUM]`. | U+22A4 | `ESC[U22A4m` | `\u22A4` |
| ⊢ | Proves — p can be derived (proved) from the premises by the rules of the system. | U+22A2 | `ESC[U22A2m` | `\u22A2` |
| ⊨ | Entails — p is true in every interpretation in which all the premises are true. | U+22A8 | `ESC[U22A8m` | `\u22A8` |
| ∴ | Therefore — marks the conclusion of an argument. | U+2234 | `ESC[U2234m` | `\u2234` |
| ∵ | Because — marks a reason or premise for a claim. | U+2235 | `ESC[U2235m` | `\u2235` |
| ⊕ | Exclusive or (circled-plus form) — true exactly when exactly one of p, q is true. No compact alias. | U+2295 | `ESC[U2295m` | `\u2295` |
| ⊻ | Exclusive or — true exactly when exactly one of p, q is true, the same connective as ⊕. No compact alias. | U+22BB | `ESC[U22BBm` | `\u22BB` |
| ↑ | Sheffer stroke (NAND) — "not (p and q)", true except when both p and q are true. No compact alias. | U+2191 | `ESC[U2191m` | `\u2191` |
| ⊬ | Does not prove — p cannot be derived from the premises. No compact alias. | U+22AC | `ESC[U22ACm` | `\u22AC` |
| ⊭ | Does not entail — p is not a semantic consequence of the premises. No compact alias. | U+22AD | `ESC[U22ADm` | `\u22AD` |

The full 18-symbol inventory, with compact aliases and long forms,
is in `references/SYMBOLS.md` and `references/logic_mapping.csv`.
Verify against those files; do not extend this list from memory.
In particular, this is sentential logic only: there are no quantifiers
in this inventory.

- ESC form: `ESC[U00ACm` — literal ESC byte (U+001B) + `[U` + 4 hex digits
  for the Basic Multilingual Plane, 6 hex digits for astral planes, + `m`.
  Example: ¬ is `ESC[U00ACm`, 😀 is `ESC[U01F600m`.
- Visible form: `\u00AC` — backslash + `u` + 4 hex digits, or `\U` + 6
  hex digits for astral planes. Example: ¬ is `\u00AC`, 😀 is `\U0001F600`.
- `--mode both` emits both; `esc-only` / `visible-only` emit one.
- Space, LF, CR: `[U+0020]` / `\u0020` for space, `[U+000A]` / `\u000A`
  for line feed, `[U+000D]` / `\u000D` for carriage return, plus readable
  aliases `[SP]`, `[LF]`, `[CR]`, `[CRLF]` in visible form only.
- Compact logic aliases (opt-in, `--logic` only): `~` ¬, `&` ∧, `|` ∨,
  `->` →, `<->` ↔, `=>` ⊃, `==` ≡, `_|_` ⊥, `T` ⊤ (see warning above),
  `|-` ⊢, `|=` ⊨, `.:.` ∴, `:.:` ∵. ⊕, ⊻, ↑, ⊬, ⊭ have no compact alias.

## How to run it (coding agents / Muse VM)

The script takes a UTF-8 file, or stdin if no file is given. `--mode`
is a global flag and goes BEFORE the subcommand; `--form` goes after
`encode` / `decode`.

1. Run: `printf '¬(p ∧ q) → r\n' | python3 scripts/ascii_unicode_code.py --mode both encode --form visible`
   (or `--form esc` for ESC form; `decode` / `convert --to visible|esc`
   work the same way; see `references/SPEC.md` and `references/HOWTO.md`.)
2. Show the script's exact output. Do not re-derive code points by hand.
3. If the script cannot run in this app, fall back to "Text-only fallback"
   below and say so.

## Text-only fallback (chat apps — no Python)

- Use `references/logic_mapping.csv` and `references/SYMBOLS.md` for logic
  symbols only.
- For any other character, state its Unicode name + code point only if you
  are certain; otherwise say "unknown — run the script" rather than guessing.

## Abstract surrogates (opt-in, code v1.1.0)

Surrogates U+D800–U+DFFF are not valid scalar values and are
rejected by default. With `--abstract-surrogates`, a surrogate
is represented only as the abstract reference
`[SURROGATE U+D800]` (plain ASCII, same in both forms).
Encoding a lone surrogate emits that token; decoding a
surrogate form (`ESC[UD800m` / `\uD800`) or the token yields
that same token — never a lone surrogate character. All 2,048
surrogates work this way; without the flag they are still
rejected.

Plainly: a lone surrogate is not a character, it is only a
code point, so the token is a reference to it, not the
character itself. A surrogate pair is different, and pair
handling is available: a high
surrogate followed at once by a low surrogate is how UTF-16
writes one astral character — the pair is one character in
another spelling, not two characters. For example, the pair
U+D83D U+DE00 is 😀 (U+1F600), and the encoder encodes it as
`\U0001F600` in both modes, with or without the flag. A lone
surrogate, a low surrogate on its own, or a high surrogate
followed by anything that is not a low surrogate is not a
pair: it is rejected by default, and becomes an abstract
token only with `--abstract-surrogates`. Decoding does not
make pairs: decoding `\U0001F600` gives 😀, and decoding two
abstract tokens gives those two tokens back.

## Do not upload the full mapping

Do NOT include `unicode_mapping.csv` (1,114,112 rows, 105 MB) in a chat-app
upload. It exceeds chat-app size and file-count limits and will be dropped
or truncated. Ship this folder (script + SPEC + logic_mapping.csv) and let
the script do Unicode lookups where it can run. The full CSV belongs beside
the skill for tier-1 coding agents / Muse's VM only, and is referenced by
path, not included here.

## Output format

- Show input, mode, ESC form, visible form, and decoded round-trip, each on
  its own line.
- Never silently drop a character you cannot encode; list it as unencoded.

## Compact prompt (paste into any chat app, ≤1,500 characters)

Adopt this code for logic/Unicode. ESC form: ESC[U00ACm (ESC=U+001B).
Visible form: \u00AC. Example: ¬ = ESC[U00ACm = \u00AC. ∧ U+2227,
∨ U+2228, → U+2192, ↔ U+2194, ⊥ U+22A5, ⊤ U+22A4. When I ask to
encode/decode/convert, use these forms exactly, never invent a code
point; if unsure, say unknown. If you can run Python, run
scripts/ascii_unicode_code.py --mode both encode --form visible
(or --form esc), reading from a file or stdin, and show its exact
output. Show input, mode, ESC form, visible form, and round-trip decode.
