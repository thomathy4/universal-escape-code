# Symbols — definitions beside the symbols

Every symbol in this code has its definition in the cell
immediately beside it, in the same row. Nothing is defined
in a separate glossary far from its symbol.

The full Unicode mapping is defined the same way in
`unicode_mapping.csv`: column 1 is the code point, column 2
is the definition or name, and every row has one — assigned
and control rows use the Unicode name, and unassigned,
surrogate, noncharacter, and private-use rows use the status
definition in the status table below.

In the tables below, `ESC` means the literal escape byte
0x1B. In the CSV files the same form is written
`<ESC>[U…m` as a printable placeholder; the real code
contains the byte 0x1B.

## The logic inventory (18 symbols)

| Symbol | Definition | Code point | Unicode name | ESC form | Visible form | Compact alias | Long form |
|---|---|---|---|---|---|---|---|
| ¬ | Negation — "not". ¬p is true exactly when p is false. | U+00AC | NOT SIGN | `ESC[U00ACm` | `\u00AC` | `~` | `[NOT]` |
| ∧ | Conjunction — "and". p ∧ q is true exactly when both p and q are true. | U+2227 | LOGICAL AND | `ESC[U2227m` | `\u2227` | `&` | `[AND]` |
| ∨ | Disjunction — "or" (inclusive). p ∨ q is true when p is true, or q is true, or both are true. | U+2228 | LOGICAL OR | `ESC[U2228m` | `\u2228` | `\|` | `[OR]` |
| → | Implication — "if … then …". p → q is false only when p is true and q is false; otherwise it is true. This is material implication. | U+2192 | RIGHTWARDS ARROW | `ESC[U2192m` | `\u2192` | `->` | `[IF]` |
| ↔ | Biconditional — "if and only if". p ↔ q is true exactly when p and q have the same truth value. | U+2194 | LEFT RIGHT ARROW | `ESC[U2194m` | `\u2194` | `<->` | `[IFF]` |
| ⊃ | Implication (alternative notation) — "if … then …", the same connective as →, in the older notation. It is not a different connective from →. | U+2283 | SUPERSET OF | `ESC[U2283m` | `\u2283` | `=>` | `[IMPLIES]` |
| ≡ | Equivalence — "is equivalent to". p ≡ q says p and q have the same truth value in every case. | U+2261 | IDENTICAL TO | `ESC[U2261m` | `\u2261` | `==` | `[EQUIV]` |
| ⊥ | Falsum — the constant false proposition, always false; also used to mark a contradiction. Also called "bottom". | U+22A5 | UP TACK | `ESC[U22A5m` | `\u22A5` | `_\|_` | `[FALSUM]` |
| ⊤ | Verum — the constant true proposition, always true. Also called "top". Warning: `T` is also a propositional variable, so use the `T` alias only in formula mode (`--logic`); in general text use the canonical form or `[VERUM]`. | U+22A4 | DOWN TACK | `ESC[U22A4m` | `\u22A4` | `T` | `[VERUM]` |
| ⊢ | Proves — "proves" / "derives". Γ ⊢ p says p can be derived (proved) from the premises Γ by the rules of the system. This is syntactic consequence, as opposed to semantic consequence (⊨). | U+22A2 | RIGHT TACK | `ESC[U22A2m` | `\u22A2` | `\|-` | `[PROVES]` |
| ⊨ | Entails — "entails" / "is a semantic consequence of". Γ ⊨ p says p is true in every interpretation in which all of Γ are true. This is semantic consequence, as opposed to syntactic proof (⊢). | U+22A8 | TRUE | `ESC[U22A8m` | `\u22A8` | `\|=` | `[ENTAILS]` |
| ∴ | Therefore — "therefore". ∴ marks the conclusion of an argument: the premises above it, therefore the conclusion after it. | U+2234 | THEREFORE | `ESC[U2234m` | `\u2234` | `.:.` | `[THEREFORE]` |
| ∵ | Because — "because". ∵ marks a reason or premise: the claim before it, because the reason after it. | U+2235 | BECAUSE | `ESC[U2235m` | `\u2235` | `:.:` | `[BECAUSE]` |
| ⊕ | Exclusive or (circled-plus form) — p ⊕ q is true exactly when exactly one of p, q is true. This is the circled-plus notation for exclusive or; ⊻ below is the other notation for the same connective. No compact alias: a single `xor` alias would collide with ⊻, so use the long form or the canonical form. | U+2295 | CIRCLED PLUS | `ESC[U2295m` | `\u2295` | — (none) | `[CIRCLED-PLUS]` |
| ⊻ | Exclusive or — p ⊻ q is true exactly when exactly one of p, q is true, the same connective as ⊕, in a different notation. No compact alias: a single `xor` alias would collide with ⊕, so use the long form or the canonical form. | U+22BB | XOR | `ESC[U22BBm` | `\u22BB` | — (none) | `[XOR]` |
| ↑ | Sheffer stroke (NAND) — p ↑ q is true except when both p and q are true; it is "not (p and q)". It is a functionally complete connective on its own. The arrow ↑ is used here as the Sheffer stroke symbol, as approved; the same code point is also the ordinary upwards arrow in other contexts. No compact alias: `\|` is already disjunction (∨) in this code, so use the long form or the canonical form. | U+2191 | UPWARDS ARROW | `ESC[U2191m` | `\u2191` | — (none) | `[SHEFFER]` |
| ⊬ | Does not prove — "does not prove". Γ ⊬ p says p cannot be derived from Γ, the negation of ⊢. No compact alias: a form such as `\|-/` would be read as `\|-` followed by `/` and would be ambiguous, so use the long form or the canonical form. | U+22AC | DOES NOT PROVE | `ESC[U22ACm` | `\u22AC` | — (none) | `[NOT-PROVES]` |
| ⊭ | Does not entail — "does not entail". Γ ⊭ p says p is not a semantic consequence of Γ, the negation of ⊨. No compact alias, for the same reason as ⊬, so use the long form or the canonical form. | U+22AD | NOT TRUE | `ESC[U22ADm` | `\u22AD` | — (none) | `[NOT-ENTAILS]` |

## Space, LF, CR — definitions beside the symbols

| Symbol | Definition | Code point | ESC form | Visible form | Alias |
|---|---|---|---|---|---|
| (space) | Space — the ordinary word space. | U+0020 | `ESC[U0020m` | `\u0020` | `[SP]` |
| (line feed) | Line feed (LF) — the new-line character. | U+000A | `ESC[U000Am` | `\u000A` | `[LF]` |
| (carriage return) | Carriage return (CR) — the return key character. | U+000D | `ESC[U000Dm` | `\u000D` | `[CR]` |
| (CRLF pair) | CRLF — the pair CR followed by LF (U+000D U+000A), the Windows-style line ending. | U+000D U+000A | `ESC[U000Dm` + LF | `\u000D` + LF | `[CRLF]` |

The symbol column for space, line feed, and carriage return
shows the name in words because the character itself is
invisible in a table. The code point column beside the
definition identifies it exactly.

## Status definitions (for the full Unicode mapping)

| Status | Definition |
|---|---|
| assigned | A character assigned in Unicode 18.0.0, with its Unicode name in the row. |
| control | A control character (U+0000–U+001F, U+007F–U+009F), with its Unicode name in the row. |
| private-use | A private-use code point; no standard character is assigned to it, and no meaning is invented. |
| unassigned | No character assigned in Unicode 18.0.0. |
| noncharacter | Permanently reserved; never a character. |
| surrogate | U+D800–U+DFFF; not a valid scalar value, not a character; encoding or decoding it is rejected. |
