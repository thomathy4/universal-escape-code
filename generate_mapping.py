#!/usr/bin/env python3
"""Generate unicode_mapping.csv and logic_mapping.csv.

Reproducible generator for the ASCII/ANSI Unicode code.
Source: UnicodeData.txt (Unicode 18.0.0, downloaded 2026-11-17 from
https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt),
kept in this folder as UnicodeData.txt. If that file is absent, falls
back to Python's unicodedata module (version recorded in the CSV header
comment is not possible in CSV, so the version is printed and recorded
in SPEC.md / TEST_REPORT.md instead; this run used UnicodeData.txt).

Output: unicode_mapping.csv — one row per code point U+0000..U+10FFFF
(1,114,112 rows), ASCII-only.
        logic_mapping.csv — sentential-logic inventory only.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCD = os.path.join(HERE, "UnicodeData.txt")
OUT = os.path.join(HERE, "unicode_mapping.csv")
LOGIC_OUT = os.path.join(HERE, "logic_mapping.csv")

TOTAL = 0x110000  # 1,114,112

LOGIC = [
    # symbol, codepoint, compact_alias, long_form
    ("\u00ac", 0x00AC, "~", "[NOT]"),
    ("\u2227", 0x2227, "&", "[AND]"),
    ("\u2228", 0x2228, "|", "[OR]"),
    ("\u2192", 0x2192, "->", "[IF]"),
    ("\u2194", 0x2194, "<->", "[IFF]"),
    ("\u2283", 0x2283, "=>", "[IMPLIES]"),
    ("\u2261", 0x2261, "==", "[EQUIV]"),
    ("\u22a5", 0x22A5, "_|_", "[FALSUM]"),
    ("\u22a4", 0x22A4, "T", "[VERUM]"),
    ("\u22a2", 0x22A2, "|-", "[PROVES]"),
    ("\u22a8", 0x22A8, "|=", "[ENTAILS]"),
    ("\u2234", 0x2234, ".:.", "[THEREFORE]"),
    ("\u2235", 0x2235, ":.:", "[BECAUSE]"),
    ("\u2295", 0x2295, "", "[CIRCLED-PLUS]"),
    ("\u22bb", 0x22BB, "", "[XOR]"),
    ("\u2191", 0x2191, "", "[SHEFFER]"),
    ("\u22ac", 0x22AC, "", "[NOT-PROVES]"),
    ("\u22ad", 0x22AD, "", "[NOT-ENTAILS]"),
]
LOGIC_BY_CP = {cp: (sym, alias, longf) for sym, cp, alias, longf in LOGIC}

# Short definition in words for each logic symbol. Column 2 of
# logic_mapping.csv (see layout rule in SPEC.md: Symbol first,
# Definition second, all other columns after).
LOGIC_DEFINITIONS = {
    0x00AC: "Negation: 'not' - true exactly when p is false",
    0x2227: "Conjunction: 'and' - true exactly when both p and q are true",
    0x2228: "Disjunction: 'or' (inclusive) - true when p or q or both are true",
    0x2192: "Implication: 'if ... then ...' - false only when p is true and q is false",
    0x2194: "Biconditional: 'if and only if' - true exactly when p and q have the same truth value",
    0x2283: "Implication (alternative notation): 'if ... then ...', same connective as U+2192",
    0x2261: "Equivalence: 'is equivalent to' - p and q have the same truth value in every case",
    0x22A5: "Falsum: the constant false proposition, always false; also marks a contradiction",
    0x22A4: "Verum: the constant true proposition, always true",
    0x22A2: "Proves: p can be derived (proved) from the premises by the rules of the system",
    0x22A8: "Entails: p is true in every interpretation in which all the premises are true",
    0x2234: "Therefore: marks the conclusion of an argument",
    0x2235: "Because: marks a reason or premise for a claim",
    0x2295: "Exclusive or (circled-plus form): true exactly when exactly one of p, q is true",
    0x22BB: "Exclusive or: true exactly when exactly one of p, q is true",
    0x2191: "Sheffer stroke (NAND): 'not (p and q)' - true except when both p and q are true",
    0x22AC: "Does not prove: p cannot be derived from the premises",
    0x22AD: "Does not entail: p is not a semantic consequence of the premises",
}

# Definition text for rows with no Unicode name. Column 2 of
# unicode_mapping.csv.
STATUS_DEFINITIONS = {
    "unassigned": "Unassigned in Unicode 18.0.0 - no character assigned",
    "surrogate": "Surrogate - not a valid scalar value, not a character",
    "noncharacter": "Noncharacter - permanently reserved, never a character",
    "private-use": "Private use - no standard character assigned",
}

NONCHAR_RANGES = [(0xFDD0, 0xFDEF)]


def is_noncharacter(cp):
    if 0xFDD0 <= cp <= 0xFDEF:
        return True
    if (cp & 0xFFFE) == 0xFFFE:  # ends FFFE or FFFF in any plane
        return True
    return False


def is_private_use(cp):
    return (0xE000 <= cp <= 0xF8FF) or (0xF0000 <= cp <= 0xFFFFD) or (0x100000 <= cp <= 0x10FFFD)


def esc_transcription2(cp):
    if cp <= 0xFFFF:
        return "<ESC>[U%04Xm" % cp
    return "<ESC>[U%06Xm" % cp


def visible_form(cp):
    if cp <= 0xFFFF:
        return "\\u%04X" % cp
    return "\\U%08X" % cp


def parse_ucd(path):
    """Return dict cp -> (name, category). Expands First/Last ranges."""
    assigned = {}
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line:
            i += 1
            continue
        fields = line.split(";")
        cp = int(fields[0], 16)
        name = fields[1]
        cat = fields[2]
        alias = fields[10] if len(fields) > 10 else ""
        if name.endswith(", First>"):
            base = name[:-len(", First>")] + ">"
            # next line is Last
            j = i + 1
            last_fields = lines[j].split(";")
            last_cp = int(last_fields[0], 16)
            # Surrogates (U+D800-U+DFFF) are listed in UnicodeData.txt
            # as a range but are NOT assigned characters / valid scalar
            # values. Do not add them to the assigned dict.
            if "surrogate" not in base.lower():
                for c in range(cp, last_cp + 1):
                    assigned[c] = (base, cat)
            i = j + 1
            continue
        if "<control>" in name and alias:
            name = "<control> (%s)" % alias
        assigned[cp] = (name, cat)
        i += 1
    return assigned


def main():
    if os.path.exists(UCD):
        assigned = parse_ucd(UCD)
        source = "UnicodeData.txt (Unicode 18.0.0)"
        print("Source: %s, assigned entries: %d" % (source, len(assigned)))
    else:
        import unicodedata
        assigned = {}
        for cp in range(TOTAL):
            try:
                name = unicodedata.name(chr(cp))
            except ValueError:
                continue
            assigned[cp] = (name, unicodedata.category(chr(cp)))
        source = "Python unicodedata %s" % unicodedata.unidata_version
        print("Source: %s, assigned entries: %d" % (source, len(assigned)))

    counts = {}
    # Layout rule (Thomas, 2026-11-17): Column 1 is the code point
    # (the symbol itself cannot be shown here, because this file is
    # ASCII-only), Column 2 is the definition/name, immediately
    # beside it. All other columns come after the definition.
    # A row never has an empty definition: assigned/control rows
    # use the Unicode name; unassigned/surrogate/noncharacter/
    # private-use rows use the status definition above.
    with open(OUT, "w", encoding="ascii", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["codepoint", "definition", "decimal", "status",
                    "esc_form", "visible_form", "logic_alias"])
        for cp in range(TOTAL):
            if 0xD800 <= cp <= 0xDFFF:
                status, name = "surrogate", ""
            elif is_noncharacter(cp):
                status, name = "noncharacter", assigned.get(cp, ("", ""))[0] if cp in assigned else ""
            elif is_private_use(cp):
                status, name = "private-use", assigned.get(cp, ("", ""))[0] if cp in assigned else ""
            elif cp in assigned:
                name, cat = assigned[cp]
                if cat == "Cc" or cp < 0x20 or cp == 0x7F or (0x80 <= cp <= 0x9F):
                    status = "control"
                else:
                    status = "assigned"
            else:
                status, name = "unassigned", ""
            definition = name if name else STATUS_DEFINITIONS[status]
            counts[status] = counts.get(status, 0) + 1
            logic_alias = LOGIC_BY_CP.get(cp, ("", "", ""))[1] if cp in LOGIC_BY_CP else ""
            w.writerow(["U+%04X" % cp if cp <= 0xFFFF else "U+%06X" % cp,
                        definition, cp, status,
                        esc_transcription2(cp), visible_form(cp), logic_alias])
    print("Wrote %s rows=%d" % (OUT, TOTAL))
    print("Status counts: %s" % counts)
    print("Total by counts: %d" % sum(counts.values()))

    # logic_mapping.csv is kept ASCII-only: the first column is the
    # visible-form transcription of the symbol (e.g. \u00AC), not the
    # raw non-ASCII glyph. Decode visible_form to recover the glyph.
    # This is a deliberate deviation from a raw-glyph column, recorded
    # in SPEC.md, so that both CSVs are ASCII-only.
    # Layout rule: Column 1 Symbol, Column 2 Definition, all other
    # columns after the definition.
    with open(LOGIC_OUT, "w", encoding="ascii", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["symbol_visible_form", "definition", "codepoint", "unicode_name", "esc_form",
                    "visible_form", "compact_alias", "long_form"])
        for sym, cp, alias, longf in LOGIC:
            name = assigned.get(cp, ("", ""))[0]
            w.writerow([visible_form(cp), LOGIC_DEFINITIONS[cp], "U+%04X" % cp, name,
                        esc_transcription2(cp), visible_form(cp), alias, longf])
    print("Wrote %s rows=%d" % (LOGIC_OUT, len(LOGIC)))


if __name__ == "__main__":
    main()
