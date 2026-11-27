#!/usr/bin/env python3
"""Build the static symbology site: HTML + SVG + JavaScript, no backend.

The site is generated from this project's own data:

    logic_mapping.csv                        the 18 logic symbols
    mapping/unicode_mapping.chunk01.csv      the printable ASCII names
    SPEC.md section 5                        space, LF, CR

Output (all static files, served by any plain file server):

    index.html              master page: every set, every combination, the learner
    units/set-*.html        one page per subset of basic units (two columns)
    combos/comb-*.html      combination pages, definitions composed by rule
    learner.html            the no-backend learner (attention + perceptron)
    data/corpus.js          units, rules and combinations, as plain JavaScript
    assets/site.css         shared styles
    assets/site.js          cookies, links, page automation, SVG helpers
    assets/learner.js       the learner: deconstruct, reconstruct, train

Run:  python3 site/build_site.py
"""

from __future__ import annotations

import csv
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
UNITS_DIR = HERE / "units"
COMBOS_DIR = HERE / "combos"
DATA_DIR = HERE / "data"

LOGIC_CSV = ROOT / "logic_mapping.csv"
ASCII_CSV = ROOT / "mapping" / "unicode_mapping.chunk01.csv"

STOP = {
    "the", "and", "or", "of", "to", "is", "are", "that", "this", "it", "in",
    "with", "as", "for", "when", "be", "by", "from", "a", "an", "at", "on",
    "its", "their", "only", "exactly", "every", "all", "can", "one", "two",
    "than", "then", "which", "same", "also", "used", "use", "not",
}


def esc(text: str) -> str:
    """Escape text for HTML."""
    return html.escape(text, quote=True)


def tokens(text: str) -> set[str]:
    """Definition tokens, for relating units to one another."""
    return {
        w for w in re.findall(r"[a-z][a-z\-]{2,}", text.lower())
        if w not in STOP
    }


# ---------------------------------------------------------------- the rules
#
# A small set of escapable rules. Each rule is one template plus the words
# that signal it; the learner scores those words by attention. "glue" is the
# literal text between the two operands (binary rules), "affix" wraps the one
# operand (unary rules), so a definition can be split back into its parts.

RULES = [
    {"id": "R1", "name": "NOT-APPLY", "op": "\u00ac", "arity": 1,
     "template": "It is not the case that {0}",
     "trigger": ["negation", "not", "false", "case"],
     "affix": r"^it is not the case that (.*?)\.?$"},
    {"id": "R2", "name": "AND-JOIN", "op": "\u2227", "arity": 2,
     "template": "{0}, and {1}",
     "trigger": ["conjunction", "and", "both", "true"],
     "glue": r",\s+and\s+"},
    {"id": "R3", "name": "OR-JOIN", "op": "\u2228", "arity": 2,
     "template": "{0}, or {1}",
     "trigger": ["disjunction", "or", "inclusive", "both"],
     "glue": r",\s+or\s+"},
    {"id": "R4", "name": "IF-JOIN", "op": "\u2192", "arity": 2,
     "template": "If {0}, then {1}",
     "trigger": ["implication", "if", "then", "false"],
     "glue": r"^if (.*?), then (.*)$"},
    {"id": "R5", "name": "IFF-JOIN", "op": "\u2194", "arity": 2,
     "template": "{0} if and only if {1}",
     "trigger": ["biconditional", "if", "only", "same", "value"],
     "glue": r"\s+if and only if\s+"},
    {"id": "R6", "name": "IMPLIES-JOIN", "op": "\u2283", "arity": 2,
     "template": "{0} implies {1}",
     "trigger": ["implication", "implies", "notation", "then"],
     "glue": r"\s+implies\s+"},
    {"id": "R7", "name": "EQUIV-JOIN", "op": "\u2261", "arity": 2,
     "template": "{0} is equivalent to {1}",
     "trigger": ["equivalence", "equivalent", "value", "every"],
     "glue": r"\s+is equivalent to\s+"},
    {"id": "R8", "name": "XOR-JOIN", "op": "\u2295", "also": ["\u22bb"], "arity": 2,
     "template": "Exactly one of {0} and {1} is true",
     "trigger": ["exclusive", "exactly", "one", "true"],
     "glue": r"^exactly one of (.*?) and (.*?) is true$"},
    {"id": "R9", "name": "NAND-JOIN", "op": "\u2191", "arity": 2,
     "template": "Not both {0} and {1}",
     "trigger": ["sheffer", "stroke", "nand", "both"],
     "glue": r"^not both (.*?) and (.*)$"},
    {"id": "R10", "name": "THEREFORE", "op": "\u2234", "arity": 2,
     "template": "{0}, therefore {1}",
     "trigger": ["therefore", "conclusion", "argument"],
     "glue": r",\s+therefore\s+"},
    {"id": "R11", "name": "BECAUSE", "op": "\u2235", "arity": 2,
     "template": "{0}, because {1}",
     "trigger": ["because", "reason", "premise", "claim"],
     "glue": r",\s+because\s+"},
    {"id": "R12", "name": "PROVES", "op": "\u22a2", "arity": 2,
     "template": "{0} proves {1}",
     "trigger": ["proves", "derived", "premises", "rules"],
     "glue": r"\s+proves\s+"},
    {"id": "R13", "name": "ENTAILS", "op": "\u22a8", "arity": 2,
     "template": "{0} entails {1}",
     "trigger": ["entails", "semantic", "consequence", "interpretation"],
     "glue": r"\s+entails\s+"},
    {"id": "R14", "name": "NOT-PROVES", "op": "\u22ac", "arity": 2,
     "template": "{0} does not prove {1}",
     "trigger": ["proves", "cannot", "derived", "negation"],
     "glue": r"\s+does not prove\s+"},
    {"id": "R15", "name": "NOT-ENTAILS", "op": "\u22ad", "arity": 2,
     "template": "{0} does not entail {1}",
     "trigger": ["entails", "consequence", "semantic", "negation"],
     "glue": r"\s+does not entail\s+"},
]

RULE_BY_OP: dict[str, dict] = {}
for _rule in RULES:
    RULE_BY_OP[_rule["op"]] = _rule
    for _also in _rule.get("also", []):
        RULE_BY_OP[_also] = _rule


def embed(text: str) -> str:
    """The ESCAPE-EMBED rule: a definition put inside another definition.

    Backslashes are doubled so an encoded form stays literal, and the guillemets
    that mark the embed are themselves neutralised.
    """
    text = text.replace("\\", "\\\\").replace("\u00ab", "\\\u00ab").replace("\u00bb", "\\\u00bb")
    return "\u00ab" + text + "\u00bb"


def compose(op_unit: dict, other_unit: dict) -> dict | None:
    """Compose two units into one definition, using the operator's rule."""
    rule = RULE_BY_OP.get(op_unit["char"])
    if rule is None:
        return None
    if rule["arity"] == 1:
        definition = rule["template"].format(embed(other_unit["def"]))
    else:
        definition = rule["template"].format("p", embed(other_unit["def"]))
    return {
        "rule": rule["id"],
        "rule_name": rule["name"],
        "definition": definition,
        "expr": op_unit["char"] + " " + other_unit["char"],
    }


def compose_sequence(a: dict, b: dict) -> dict:
    """COMPOSE: the fallback rule, used where no operator rule applies."""
    return {
        "rule": "R0",
        "rule_name": "COMPOSE",
        "definition": embed(a["def"]) + " then " + embed(b["def"]),
        "expr": a["char"] + " " + b["char"],
    }


# ---------------------------------------------------------------- the units

def unit(cp: int, name: str, definition: str, family: str,
         alias: str = "", long_form: str = "") -> dict:
    digits = 4 if cp <= 0xFFFF else 6
    return {
        "id": "%04X" % cp if cp <= 0xFFFF else "%06X" % cp,
        "char": chr(cp),
        "name": name,
        "cp": "U+%0*X" % (digits, cp),
        "esc": "<ESC>[U%0*Xm" % (digits, cp),
        "vis": "\\u%0*X" % (digits, cp),
        "alias": alias,
        "long": long_form,
        "def": definition,
        "family": family,
    }


def load_logic() -> list[dict]:
    units = []
    with open(LOGIC_CSV, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            cp = int(row["codepoint"][2:], 16)
            definition = row["definition"].replace(" - ", " \u2014 ").strip()
            units.append(unit(cp, row["unicode_name"], definition, "logic",
                              alias=row["compact_alias"], long_form=row["long_form"]))
    return units


def load_whitespace() -> list[dict]:
    rows = [
        (0x0020, "SPACE",
         "The ordinary word space. In an encoded stream it stays the literal byte 0x20.",
         "[SP]"),
        (0x000A, "LINE FEED",
         "The new-line character. Literal in an encoded stream when newlines are preserved, "
         "which is the default; encoded otherwise.",
         "[LF]"),
        (0x000D, "CARRIAGE RETURN",
         "The return key character. Always encoded, so a CRLF pair round-trips as the CR code "
         "followed by a literal line feed.",
         "[CR]"),
    ]
    return [unit(cp, name, text, "whitespace", long_form=alias)
            for cp, name, text, alias in rows]


def load_ascii() -> list[dict]:
    units = []
    with open(ASCII_CSV, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            cp = int(row["codepoint"][2:], 16)
            if not 0x21 <= cp <= 0x7E:
                continue
            name = row["definition"].strip()
            definition = ("%s: the printable ASCII character at %s, encoded as %s."
                          % (name.capitalize(), row["codepoint"], row["visible_form"]))
            units.append(unit(cp, name, definition, "ascii"))
    return units


def glyph(u: dict) -> str:
    """A visible stand-in for a unit's character."""
    if u["char"] == " ":
        return "\u2420"
    if u["char"] == "\n":
        return "\u240a"
    if u["char"] == "\r":
        return "\u240d"
    return u["char"]


def build_sets(all_units: dict[str, dict]) -> list[dict]:
    logic = [u for u in all_units.values() if u["family"] == "logic"]
    by_char = {u["char"]: u for u in logic}
    pick = lambda chars: [by_char[c] for c in chars]

    whitespace = [u for u in all_units.values() if u["family"] == "whitespace"]
    ascii_units = sorted((u for u in all_units.values() if u["family"] == "ascii"),
                         key=lambda u: int(u["id"], 16))
    ascii_by_cp = {int(u["id"], 16): u for u in ascii_units}
    rng = lambda lo, hi: [ascii_by_cp[c] for c in range(lo, hi + 1) if c in ascii_by_cp]

    return [
        {"id": "set-01-connectives", "short": "Connectives", "title": "Connectives \u2014 the core five",
         "blurb": "The five connectives every formula is built from: not, and, or, "
                  "if\u2026then, if and only if.",
         "units": pick("\u00ac\u2227\u2228\u2192\u2194")},
        {"id": "set-02-constants", "short": "Equivalence", "title": "Equivalence and the constants",
         "blurb": "The older implication sign, equivalence, and the two constants "
                  "that need no operand.",
         "units": pick("\u2283\u2261\u22a5\u22a4")},
        {"id": "set-03-proof", "short": "Proof", "title": "Proof and consequence",
         "blurb": "What follows from what: syntactic proof, semantic entailment, "
                  "and the two negations of them.",
         "units": pick("\u22a2\u22a8\u22ac\u22ad")},
        {"id": "set-04-argument", "short": "Argument", "title": "Argument and alternative connectives",
         "blurb": "The marks of an argument, plus exclusive or and the Sheffer "
                  "stroke, each with a notation of its own.",
         "units": pick("\u2234\u2235\u2295\u22bb\u2191")},
        {"id": "set-05-whitespace", "short": "Whitespace", "title": "Space, line feed, carriage return",
         "blurb": "The three characters that carry no ink and still change the meaning "
                  "of a stream.",
         "units": whitespace},
        {"id": "set-06-punctuation", "short": "ASCII punctuation", "title": "Printable ASCII \u2014 punctuation",
         "blurb": "Every printable ASCII mark that is not a letter or a digit.",
         "units": rng(0x21, 0x2F) + rng(0x3A, 0x40) + rng(0x5B, 0x60) + rng(0x7B, 0x7E)},
        {"id": "set-07-digits", "short": "ASCII digits", "title": "Printable ASCII \u2014 digits",
         "blurb": "The ten digit characters, each one a unit with its own code.",
         "units": rng(0x30, 0x39)},
        {"id": "set-08-uppercase", "short": "ASCII capitals", "title": "Printable ASCII \u2014 capitals",
         "blurb": "The twenty-six capital letters.",
         "units": rng(0x41, 0x5A)},
        {"id": "set-09-lowercase", "short": "ASCII small letters", "title": "Printable ASCII \u2014 small letters",
         "blurb": "The twenty-six small letters.",
         "units": rng(0x61, 0x7A)},
    ]


def related(units: list[dict], u: dict, limit: int = 3) -> list[tuple[dict, float]]:
    """Units whose definitions share the most words with this one."""
    mine = tokens(u["def"])
    scored = []
    for other in units:
        if other["id"] == u["id"]:
            continue
        theirs = tokens(other["def"])
        union = mine | theirs
        if not union:
            continue
        score = len(mine & theirs) / len(union)
        if score > 0.08:
            scored.append((other, score))
    scored.sort(key=lambda pair: (-pair[1], pair[0]["id"]))
    return scored[:limit]


# ---------------------------------------------------------------- the pages

PAGES: list[dict] = []


def head(title: str, depth: int, page_id: str, kind: str) -> str:
    prefix = "../" * depth
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{esc(title)}</title>\n"
        f"<link rel=\"stylesheet\" href=\"{prefix}assets/site.css\">\n"
        "</head>\n"
        f"<body data-page=\"{esc(page_id)}\" data-kind=\"{esc(kind)}\">\n"
    )


def topbar(page_id: str, depth: int) -> str:
    prefix = "../" * depth
    ids = [p["id"] for p in PAGES]
    i = ids.index(page_id) if page_id in ids else 0
    prev_page = PAGES[i - 1] if i > 0 else None
    next_page = PAGES[i + 1] if i + 1 < len(PAGES) else None
    nav = []
    if prev_page:
        nav.append(f"<a class=\"navlink\" rel=\"prev\" href=\"{prefix}{prev_page['href']}\">"
                   f"\u2190 {esc(prev_page['short'])}</a>")
    if next_page:
        nav.append(f"<a class=\"navlink\" rel=\"next\" href=\"{prefix}{next_page['href']}\">"
                   f"{esc(next_page['short'])} \u2192</a>")
    return (
        "<header class=\"topbar\">\n"
        f"  <a class=\"brand\" href=\"{prefix}index.html\">Symbology</a>\n"
        f"  <nav class=\"pagenav\">{''.join(nav)}</nav>\n"
        "  <div class=\"cookiebar\" id=\"cookiebar\" aria-live=\"polite\"></div>\n"
        "</header>\n"
    )


def foot(depth: int, scripts: list[str]) -> str:
    prefix = "../" * depth
    tags = "".join(
        f"<script src=\"{prefix}{s if '/' in s else 'assets/' + s}\"></script>\n"
        for s in scripts
    )
    return (
        "<footer class=\"foot\">\n"
        "  <p>Generated by <code>site/build_site.py</code> from this project's own "
        "symbol data. Every page is plain HTML, SVG and JavaScript \u2014 nothing here "
        "needs a server to think.</p>\n"
        f"  <p><a href=\"{prefix}index.html\">Master page</a> \u00b7 "
        f"<a href=\"{prefix}learner.html\">The learner</a></p>\n"
        "</footer>\n"
        f"{tags}</body>\n</html>\n"
    )


def delineator() -> str:
    """A row's delineator, drawn as SVG rather than a border."""
    return ('<svg class="delin" viewBox="0 0 12 40" aria-hidden="true" focusable="false">'
            '<line x1="6" y1="0" x2="6" y2="40"/><line x1="2" y1="20" x2="10" y2="20"/>'
            '</svg>')


def tree_svg(rule_name: str, left: str, right: str | None) -> str:
    """A derivation, drawn as SVG: rule above, operands below."""
    if right is None:
        return (
            '<svg class="tree" viewBox="0 0 240 84" role="img" '
            f'aria-label="derivation: {esc(rule_name)}">'
            '<line x1="120" y1="26" x2="120" y2="58"/>'
            f'<text class="t-rule" x="120" y="16">{esc(rule_name)}</text>'
            f'<text class="t-node" x="120" y="76">{esc(left)}</text>'
            '</svg>'
        )
    return (
        '<svg class="tree" viewBox="0 0 240 84" role="img" '
        f'aria-label="derivation: {esc(rule_name)}">'
        '<line x1="120" y1="26" x2="56" y2="58"/><line x1="120" y1="26" x2="184" y2="58"/>'
        f'<text class="t-rule" x="120" y="16">{esc(rule_name)}</text>'
        f'<text class="t-node" x="56" y="76">{esc(left)}</text>'
        f'<text class="t-node" x="184" y="76">{esc(right)}</text>'
        '</svg>'
    )


def relation_svg(units: list[dict], edges: list[tuple[str, str]]) -> str:
    """The page's units as nodes, with lines for the definitions they share."""
    if len(units) < 2:
        return ""
    import math
    width, height = 720, 260
    cx, cy = width / 2, height / 2
    rx, ry = width / 2 - 60, height / 2 - 42
    pos = {}
    for i, u in enumerate(units):
        angle = -math.pi / 2 + (2 * math.pi * i / len(units))
        pos[u["id"]] = (cx + rx * math.cos(angle), cy + ry * math.sin(angle))
    parts = [f'<svg class="map" viewBox="0 0 {width} {height}" role="img" '
             'aria-label="units on this page and the definitions they share">']
    for a, b in edges:
        if a in pos and b in pos:
            (x1, y1), (x2, y2) = pos[a], pos[b]
            parts.append(f'<line class="edge" x1="{x1:.1f}" y1="{y1:.1f}" '
                         f'x2="{x2:.1f}" y2="{y2:.1f}"/>')
    for u in units:
        x, y = pos[u["id"]]
        parts.append(
            f'<a href="#u-{u["id"]}" class="node">'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="17"/>'
            f'<text x="{x:.1f}" y="{y + 6:.1f}">{esc(glyph(u))}</text>'
            f'<title>{esc(u["name"])}</title></a>'
        )
    parts.append('</svg>')
    return "".join(parts)


def unit_row(u: dict, page_units: list[dict], depth: int) -> str:
    rel = related(page_units, u)
    rel_html = ""
    if rel:
        links = []
        for other, score in rel:
            links.append(f'<a href="#u-{other["id"]}" title="shared definition words: '
                         f'{int(round(score * 100))}%">{esc(glyph(other))}</a>')
        rel_html = f'<p class="rel">related: {" ".join(links)}</p>'
    forms = f'<code>{esc(u["esc"])}</code> <code>{esc(u["vis"])}</code>'
    extras = []
    if u["alias"]:
        extras.append(f'alias <code>{esc(u["alias"])}</code>')
    if u["long"]:
        extras.append(f'long form <code>{esc(u["long"])}</code>')
    extra_html = f'<p class="alias">{" \u00b7 ".join(extras)}</p>' if extras else ""
    return (
        f'<tr class="row" id="u-{u["id"]}" data-unit="{u["id"]}" tabindex="0">\n'
        f'  <th class="cell" scope="row">\n'
        f'    <span class="cell-name">{esc(u["name"])}</span>\n'
        f'    <span class="cell-cp">{esc(u["cp"])}</span>\n'
        f'  </th>\n'
        f'  <td class="sym">{delineator()}<span class="glyph">{esc(glyph(u))}</span>'
        f'<span class="forms">{forms}</span></td>\n'
        f'  <td class="def"><p>{esc(u["def"])}</p>{extra_html}{rel_html}</td>\n'
        f'</tr>\n'
    )


def unit_page(s: dict, all_units: list[dict], depth: int) -> str:
    page_id = f"units/{s['id']}.html"
    units = s["units"]
    edges = set()
    for u in units:
        for other, _score in related(units, u, limit=2):
            edges.add(tuple(sorted((u["id"], other["id"]))))
    rows = "".join(unit_row(u, units, depth) for u in units)
    count = len(units)
    body = (
        topbar(page_id, depth)
        + "<main>\n"
        + f"<p class=\"crumb\"><a href=\"{'../' * depth}index.html\">master page</a> / "
          f"unit set</p>\n"
        + f"<h1>{esc(s['title'])}</h1>\n"
        + f"<p class=\"lede\">{esc(s['blurb'])} {count} units. Each row is one cell: "
          "the encoded character on the left, under its name, and its definition on the right.</p>\n"
        + "<div class=\"toolbar\">\n"
        + "  <button type=\"button\" data-walk=\"start\">Walk this page</button>\n"
        + "  <button type=\"button\" data-walk=\"stop\">Stop</button>\n"
        + "  <span class=\"hint\">or press <kbd>j</kbd> / <kbd>k</kbd> to move, "
          "<kbd>Enter</kbd> to follow the first related unit.</span>\n"
        + "</div>\n"
        + f"<figure class=\"figure\">{relation_svg(units, sorted(edges))}"
          "<figcaption>Lines join units whose definitions share words. "
          "A node is a link to its row.</figcaption></figure>\n"
        + "<table class=\"grid\">\n<caption>"
        + f"{esc(s['title'])} \u2014 {count} units</caption>\n<tbody>\n"
        + rows
        + "</tbody>\n</table>\n"
        + "</main>\n"
        + foot(depth, ["site.js"])
    )
    return head(s["title"], depth, page_id, "units") + body


def combo_rows(units: list[dict]) -> list[dict]:
    rows = []
    for a in units:
        for b in units:
            if a["id"] == b["id"]:
                continue
            composed = compose(a, b)
            if composed is None:
                continue
            rows.append({"a": a, "b": b, "composed": composed})
    if not rows:  # no operator in this set: use the fallback rule on pairs
        for i, a in enumerate(units):
            for b in units[i + 1:]:
                rows.append({"a": a, "b": b, "composed": compose_sequence(a, b)})
    return rows


def combo_page(s: dict, depth: int) -> str:
    page_id = f"combos/comb-{s['id'][4:]}.html"
    rows_data = combo_rows(s["units"])
    rows = []
    for index, row in enumerate(rows_data):
        a, b, composed = row["a"], row["b"], row["composed"]
        rows.append(
            f'<tr class="row" id="c-{index}" data-combo="{index}" tabindex="0">\n'
            f'  <th class="cell" scope="row">\n'
            f'    <span class="cell-name">{esc(composed["rule_name"])}</span>\n'
            f'    <span class="cell-cp">{esc(composed["rule"])}</span>\n'
            f'  </th>\n'
            f'  <td class="sym">{delineator()}'
            f'<span class="glyph glyph-pair">{esc(glyph(a))}{esc(glyph(b))}</span>'
            f'<span class="forms"><code>{esc(a["vis"])}</code> <code>{esc(b["vis"])}</code></span></td>\n'
            f'  <td class="def"><p>{esc(composed["definition"])}</p>'
            f'{tree_svg(composed["rule_name"], glyph(a), glyph(b))}'
            f'<p class="rel">from <a href="../units/{s["unit_page"]}#u-{a["id"]}">{esc(glyph(a))}</a> '
            f'<a href="../units/{s["unit_page"]}#u-{b["id"]}">{esc(glyph(b))}</a> \u00b7 '
            f'<button type="button" class="deconstruct" data-expr="{esc(composed["definition"])}">'
            f'deconstruct</button></p></td>\n'
            f'</tr>\n'
        )
    rules_list = "".join(
        f'<li><code>{esc(r["id"])}</code> <strong>{esc(r["name"])}</strong> '
        f'<code>{esc(r["template"])}</code></li>'
        for r in RULES if any(r is RULE_BY_OP.get(u["char"]) for u in s["units"])
    )
    body = (
        topbar(page_id, depth)
        + "<main>\n"
        + f"<p class=\"crumb\"><a href=\"{'../' * depth}index.html\">master page</a> / "
          "combination set</p>\n"
        + f"<h1>Combinations \u2014 {esc(s['title'])}</h1>\n"
        + "<p class=\"lede\">Every combination of two units from "
          f"<a href=\"../units/{s['unit_page']}\">{esc(s['title'])}</a>. The definition on "
          "the right is generated by applying the first unit's rule to the second unit's "
          "definition, looked up on the unit page. <code>p</code> and <code>q</code> stand "
          "for the operands still left open.</p>\n"
        + "<div class=\"toolbar\">\n"
        + "  <button type=\"button\" data-walk=\"start\">Walk this page</button>\n"
        + "  <button type=\"button\" data-walk=\"stop\">Stop</button>\n"
        + f"  <span class=\"hint\">{len(rows_data)} combinations \u00b7 "
          "<kbd>j</kbd> / <kbd>k</kbd> to move</span>\n"
        + "</div>\n"
        + "<section class=\"rules\">\n<h2>The rules used here</h2>\n"
        + "<ol class=\"rulelist\">" + rules_list + "</ol>\n"
        + "<p class=\"hint\">Embedding a definition inside another follows the "
          "<strong>ESCAPE-EMBED</strong> rule: backslashes are doubled so an encoded form "
          "stays literal, the guillemets <code>\u00ab \u00bb</code> mark the embed, and a "
          "guillemet inside it is neutralised.</p>\n</section>\n"
        + "<table class=\"grid\">\n<caption>"
        + f"{esc(s['title'])} \u2014 {len(rows_data)} combinations</caption>\n<tbody>\n"
        + "".join(rows)
        + "</tbody>\n</table>\n</main>\n"
        + foot(depth, ["site.js"])
    )
    return head("Combinations \u2014 " + s["title"], depth, page_id, "combos") + body


def master_page(sets: list[dict], combos: list[dict], depth: int) -> str:
    page_id = "index.html"
    set_cards = []
    for s in sets:
        glyphs = " ".join(esc(glyph(u)) for u in s["units"][:14])
        more = "" if len(s["units"]) <= 14 else f' \u2026 {len(s["units"]) - 14} more'
        set_cards.append(
            f'<li class="card"><a href="units/{s["id"]}.html"><h3>{esc(s["title"])}</h3></a>'
            f'<p class="glyphs">{glyphs}{more}</p>'
            f'<p class="meta">{len(s["units"])} units</p></li>'
        )
    combo_cards = []
    for c in combos:
        combo_cards.append(
            f'<li class="card"><a href="combos/comb-{c["id"][4:]}.html"><h3>{esc(c["title"])}</h3></a>'
            f'<p class="meta">{c["count"]} combinations \u00b7 same two columns, '
            f'definitions composed by rule</p></li>'
        )
    # the master map: unit sets on the left, combinations in the middle, the learner right
    width, height = 940, 430
    lx, mx, rx = 150, 480, 820
    set_y = {s["id"]: 30 + i * 44 for i, s in enumerate(sets)}
    combo_y = {c["id"]: 70 + i * 76 for i, c in enumerate(combos)}
    nodes = []
    edges = []
    for s in sets:
        nodes.append((f"units/{s['id']}.html", lx, set_y[s["id"]], s["short"]))
    for c in combos:
        nodes.append((f"combos/comb-{c['id'][4:]}.html", mx, combo_y[c["id"]],
                      "Combinations: " + c["short"]))
        edges.append((lx + 100, set_y[c["id"]], mx - 100, combo_y[c["id"]]))
    nodes.append(("learner.html", rx, 210, "The learner"))
    if combos:
        edges.append((mx + 100, 210, rx - 100, 210))
    map_parts = [f'<svg class="map master" viewBox="0 0 {width} {height}" role="img" '
                 'aria-label="the site: unit sets, combination sets, the learner">']
    if sets:
        map_parts.append(
            f'<line class="spine" x1="{lx - 104}" y1="{set_y[sets[0]["id"]]}" '
            f'x2="{lx - 104}" y2="{set_y[sets[-1]["id"]]}"/>')
    for x1, y1, x2, y2 in edges:
        map_parts.append(f'<line class="edge" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    for href, x, y, label in nodes:
        map_parts.append(
            f'<a href="{esc(href)}" class="node wide">'
            f'<rect x="{x - 96}" y="{y - 15}" width="192" height="30" rx="15"/>'
            f'<text x="{x}" y="{y + 5}">{esc(label)}</text>'
            f'<title>{esc(label)}</title></a>'
        )
    map_parts.append('</svg>')

    body = (
        topbar(page_id, depth)
        + "<main>\n"
        + "<h1>Symbology \u2014 the code, one cell at a time</h1>\n"
        + "<p class=\"lede\">Every unit of this code has a cell: the encoded character under "
          "its name on the left, its definition on the right. Units are grouped into sets; "
          "each set has a page. Combinations of the units in a set have pages of their own, "
          "where the definition is generated from the units' own definitions by a small set "
          "of rules. Everything is HTML, SVG and JavaScript \u2014 there is no backend, and "
          "the pages remember you with cookies.</p>\n"
        + "<div class=\"toolbar\">\n"
        + "  <button type=\"button\" data-tour=\"start\">Start the tour</button>\n"
        + "  <button type=\"button\" data-tour=\"stop\">Stop the tour</button>\n"
        + "  <a class=\"navlink\" id=\"continue\" href=\"units/set-01-connectives.html\">"
          "Continue where you left off</a>\n"
        + "</div>\n"
        + f"<figure class=\"figure\">{''.join(map_parts)}"
          "<figcaption>The whole site as one drawing: sets on the left, their combinations "
          "in the middle, the learner on the right. Every shape is a link.</figcaption></figure>\n"
        + "<h2>Unit sets</h2>\n<ul class=\"cards\">\n" + "".join(set_cards) + "</ul>\n"
        + "<h2>Combination sets</h2>\n<p class=\"hint\">The next set of pages: two units "
          "from one set, one cell, and a definition generated by rule.</p>\n"
          "<ul class=\"cards\">\n" + "".join(combo_cards) + "</ul>\n"
        + "<h2>The learner</h2>\n<ul class=\"cards\">\n"
        + '<li class="card"><a href="learner.html"><h3>Reconstruct a sentential definition</h3></a>'
          '<p class="meta">Deconstruct a definition to its basic units, rebuild it, and train '
          'the attention weights. Weights and scores live in a cookie.</p></li>\n</ul>\n'
        + "<h2>How the cells are related</h2>\n"
        + "<ul class=\"notes\">\n"
        + "<li><strong>Links.</strong> A unit links to the units whose definitions share words "
          "with it, to its own row, and to the combination page built from it.</li>\n"
        + "<li><strong>Cookies.</strong> The pages remember which units you have visited, "
          "which row you were on, the tour position, and the learner's weights.</li>\n"
        + "<li><strong>Page automation.</strong> <em>Walk this page</em> moves down the cells "
          "on a timer; <kbd>j</kbd> and <kbd>k</kbd> move by hand; the tour follows the links "
          "from set to set.</li>\n"
        + "<li><strong>Wrapping HTML.</strong> The cell is the unit: a title cell, an encoded "
          "character cell, and a definition cell, in that order, in one row.</li>\n"
        + "</ul>\n"
        + "</main>\n"
        + foot(depth, ["site.js"])
    )
    return head("Symbology \u2014 the code, one cell at a time", depth, page_id, "master") + body


def learner_page(depth: int) -> str:
    page_id = "learner.html"
    body = (
        topbar(page_id, depth)
        + "<main>\n"
        + "<p class=\"crumb\"><a href=\"index.html\">master page</a> / the learner</p>\n"
        + "<h1>The learner \u2014 deconstruct, reconstruct, train</h1>\n"
        + "<p class=\"lede\">A definition is a sentence built from basic units. This page "
          "takes one apart to its units, rebuilds it from those units, and shows the weights "
          "it used. There is no server: the model is a single attention over the rules, a "
          "softmax, and a perceptron update \u2014 all of it in this page, saved in a cookie.</p>\n"
        + "<section class=\"panel\">\n<h2>1. A sentential definition</h2>\n"
        + "<label for=\"ldef\">Definition</label>\n"
        + "<textarea id=\"ldef\" rows=\"3\" spellcheck=\"false\"></textarea>\n"
        + "<div class=\"toolbar\">\n"
        + "  <button type=\"button\" id=\"ldeconstruct\" class=\"primary\">Deconstruct</button>\n"
        + "  <button type=\"button\" id=\"lreconstruct\">Reconstruct</button>\n"
        + "  <button type=\"button\" id=\"lexample\">Load an example</button>\n"
        + "  <button type=\"button\" id=\"lreset\">Reset the model</button>\n"
        + "</div>\n"
        + "<p class=\"status\" id=\"lstatus\" role=\"status\" aria-live=\"polite\"></p>\n"
        + "</section>\n"
        + "<section class=\"panel\">\n<h2>2. Decomposition \u2014 the tree</h2>\n"
        + "<div id=\"ltree\" class=\"treebox\"></div>\n"
        + "<p class=\"hint\" id=\"lfidelity\"></p>\n"
        + "</section>\n"
        + "<section class=\"panel\">\n<h2>3. Attention over the rules</h2>\n"
        + "<div id=\"lattn\" class=\"bars\"></div>\n"
        + "<p class=\"hint\">The bars are the softmax over rule scores: what the model "
          "thinks each rule is worth for this sentence.</p>\n"
        + "<div class=\"toolbar\" id=\"lfeedback\">\n"
        + "  <span class=\"hint\">Was the top rule right?</span>\n"
        + "  <button type=\"button\" data-feedback=\"1\">Right \u2014 train</button>\n"
        + "  <button type=\"button\" data-feedback=\"0\">Wrong \u2014 train the other way</button>\n"
        + "</div>\n"
        + "</section>\n"
        + "<section class=\"panel\">\n<h2>4. Model and score</h2>\n"
        + "<div id=\"lstats\" class=\"stats\"></div>\n"
        + "<pre id=\"lmodel\" class=\"model\"></pre>\n"
        + "</section>\n"
        + "</main>\n"
        + foot(depth, ["site.js", "data/corpus.js", "learner.js"])
    )
    return head("The learner", depth, page_id, "learner") + body


# ---------------------------------------------------------------- the build

def build() -> None:
    logic = load_logic()
    whitespace = load_whitespace()
    ascii_units = load_ascii()

    all_units: dict[str, dict] = {}
    for u in logic + whitespace + ascii_units:
        all_units[u["id"]] = u

    sets = build_sets(all_units)
    for s in sets:
        s["unit_page"] = f"{s['id']}.html"

    combos = []
    for s in sets:
        if not any(u["family"] == "logic" or u["family"] == "whitespace" for u in s["units"]):
            continue
        rows = combo_rows(s["units"])
        combos.append({"id": s["id"], "title": s["title"], "short": s["short"],
                       "count": len(rows), "unit_page": s["unit_page"]})

    # the reading order: master, sets, combinations, learner
    PAGES.clear()
    PAGES.append({"id": "index.html", "href": "index.html", "short": "Master page"})
    for s in sets:
        PAGES.append({"id": f"units/{s['id']}.html", "href": f"units/{s['id']}.html",
                      "short": s["short"]})
    for c in combos:
        PAGES.append({"id": f"combos/comb-{c['id'][4:]}.html",
                      "href": f"combos/comb-{c['id'][4:]}.html",
                      "short": "Combinations: " + c["short"]})
    PAGES.append({"id": "learner.html", "href": "learner.html", "short": "The learner"})

    for directory in (UNITS_DIR, COMBOS_DIR, DATA_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    (HERE / "index.html").write_text(master_page(sets, combos, 0), encoding="utf-8")
    (HERE / "learner.html").write_text(learner_page(0), encoding="utf-8")
    for s in sets:
        (UNITS_DIR / f"{s['id']}.html").write_text(
            unit_page(s, list(all_units.values()), 1), encoding="utf-8")
    for s in sets:
        if not any(c["id"] == s["id"] for c in combos):
            continue
        (COMBOS_DIR / f"comb-{s['id'][4:]}.html").write_text(combo_page(s, 1), encoding="utf-8")

    corpus = {
        "units": [
            {"id": u["id"], "char": u["char"], "name": u["name"], "def": u["def"],
             "vis": u["vis"], "family": u["family"]}
            for u in all_units.values()
        ],
        "rules": [
            {"id": r["id"], "name": r["name"], "op": r["op"], "arity": r["arity"],
             "template": r["template"], "trigger": r["trigger"],
             "glue": r.get("glue"), "affix": r.get("affix"),
             "also": r.get("also", [])}
            for r in RULES
        ],
        "combos": [
            {"rule": row["composed"]["rule"],
             "a": row["a"]["id"], "b": row["b"]["id"],
             "expr": row["composed"]["expr"],
             "definition": row["composed"]["definition"]}
            for s in sets if any(c["id"] == s["id"] for c in combos)
            for row in combo_rows(s["units"])
        ],
        "pages": [{"id": p["id"], "href": p["href"], "short": p["short"]} for p in PAGES],
    }
    (DATA_DIR / "corpus.js").write_text(
        "window.AUC = " + json.dumps(corpus, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")

    print("wrote %d unit pages, %d combination pages, %d units, %d combinations"
          % (len(sets), len(combos), len(all_units), len(corpus["combos"])))


if __name__ == "__main__":
    build()
