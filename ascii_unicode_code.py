#!/usr/bin/env python3
"""ASCII/ANSI code for Unicode + sentential logic — encoder/decoder.

Approved design (Thomas, 2026-11-17), modes: both (primary), esc-only,
visible-only.

ASCII-only: every encoded output contains bytes 0x00-0x7F only.

Forms
-----
ESC form (literal ESC bytes):
    ESC (0x1B) '[' 'U' + hex + 'm'
    BMP   (U+0000..U+FFFF):     4 hex digits, e.g. ESC[U00ACm  for U+00AC
    Astral (U+10000..U+10FFFF): 6 hex digits, e.g. ESC[U01F600m for U+1F600
Visible form (printable text):
    BMP:    \\uXXXX,     e.g. \\u00AC
    Astral: \\U00XXXXXX (8 hex digits), e.g. \\U0001F600

Printable ASCII (0x20-0x7E) stays literal, except:
  - visible form: backslash '\\' encodes as '\\\\' (two backslashes).
    ESC form: backslash is literal 0x5C, no escape is needed or used.
  - space (0x20) stays literal in an encoded stream; LF (0x0A) stays
    literal when --preserve-newlines (default). The encoded forms
    ESC[U0020m / \\u0020, ESC[U000Am / \\u000A, ESC[U000Dm / \\u000D
    are for when the character is being *named* as a code point
    (see encode_char / named forms), not for ordinary text.
    With --no-preserve-newlines, LF and CR are both encoded.
    CR (0x0D) is always encoded in text mode (never literal), so
    CRLF round-trips as ESC[U000Dm + LF (or \\u000D + LF).

Readable aliases (visible form only, opt-in with --aliases):
    [SP] -> U+0020, [LF] -> U+000A, [CR] -> U+000D, [CRLF] -> U+000D U+000A
    Logic long forms: [NOT] [AND] [OR] [IF] [IFF] [IMPLIES] [EQUIV]
    [FALSUM] [VERUM] [PROVES] [ENTAILS] [THEREFORE] [BECAUSE]
    [CIRCLED-PLUS] [XOR] [SHEFFER] [NOT-PROVES] [NOT-ENTAILS]
    Aliases are decoded only with --aliases, and are never emitted
    by the plain encoder, so ordinary text containing "[SP]" is not
    silently rewritten by default.

Sentential-logic compact aliases (opt-in with --logic, default off):
    ¬ ~  ∧ &  ∨ |  → ->  ↔ <->  ⊃ =>  ≡ ==  ⊥ _|_  ⊤ T  ⊢ |-  ⊨ |=
    ∴ .:.  ∵ :.:  ⊕ (none)  ⊻ (none)  ↑ Sheffer (none)
    ⊬ (none)  ⊭ (none)
    "None" means no safe compact alias exists (collision); the long
    form or the canonical ESC/visible form must be used instead.
    WARNING — T collision: 'T' is both verum (⊤) and a propositional
    variable. --logic decoding maps a bare 'T' to ⊤ only in formula
    mode; do not use --logic on general text. Likewise '~', '&', '|'
    are ordinary ASCII in general text; --logic is for formulas only.

Surrogates (U+D800-U+DFFF) are not valid scalar values: encoding or
decoding them is rejected with a clear error — unless the opt-in
abstract surrogate mode is used (see below). Code points above
U+10FFFF are likewise rejected.

Abstract surrogate mode (opt-in, --abstract-surrogates):
    A surrogate on its own is never a character and can never
    round-trip as text. In abstract mode a lone surrogate code
    point is represented only as an abstract reference, the
    plain-ASCII token [SURROGATE U+D800] (same token in both
    forms, uppercase hex, 4 digits). Encoding a lone surrogate
    emits that token; decoding a canonical surrogate form
    (ESC[UD800m / \uD800) or the token itself yields that same
    token — never a lone surrogate character — so every output
    stays valid ASCII/UTF-8. This mode is off by default;
    without it, lone surrogates are rejected exactly as before.
    It exists so a document can mention and embed all 2,048
    surrogate code points without breaking, and without
    pretending they are valid characters.
    CLI encode reads its input as UTF-8; with the flag it reads
    with errors="surrogatepass", so CESU-8/WTF-8 surrogate byte
    sequences (ED A0 80 etc.) become lone surrogates and then
    abstract tokens. Ordinary UTF-8 text is unaffected.

Surrogate pairs (plain truth, in both modes):
    A pair is different from a lone surrogate. A high surrogate
    (U+D800–U+DBFF) followed at once by a low surrogate
    (U+DC00–U+DFFF) is how UTF-16 writes ONE astral character:
    the pair is not two characters, it is one character in
    another spelling. For example, the pair U+D83D U+DE00 is
    the character 😀 (U+1F600). So encode_text combines a
    valid pair into that astral character and encodes it in
    the ordinary way (\U0001F600 / ESC[U01F600m), in both
    modes, with or without --abstract-surrogates. A lone
    surrogate, a low surrogate on its own, or a high surrogate
    followed by anything that is not a low surrogate is not a
    pair: it is rejected by default, and becomes an abstract
    token only with --abstract-surrogates. Decoding does not
    make pairs: decoding \U0001F600 gives 😀, and decoding
    two abstract tokens gives those two tokens back, because
    a token is a reference to a code point, not a character.

Modes
-----
--mode both (default, primary): encoder may emit either form
    (--form esc|visible), decoder accepts both, convert works both ways.
--mode esc-only: only the ESC form is the code. Encoder emits ESC
    form only (--form visible is an error). Decoder accepts ESC form
    only; a visible \\u sequence in the input is left literal, not
    decoded. Convert --to visible is an error.
--mode visible-only: only the visible form is the code. Encoder emits
    visible form only (--form esc is an error). Decoder accepts visible
    form only; a literal ESC byte in the input is an error. Convert
    --to esc is an error.

Stdlib only. Python 3.8+.
"""
import argparse
import re
import sys

ESC = "\x1b"
VERSION = "1.1.0"
UNICODE_VERSION = "18.0.0"

# ---------------------------------------------------------------- logic
LOGIC_BY_CHAR = {
    "\u00ac": "~", "\u2227": "&", "\u2228": "|", "\u2192": "->",
    "\u2194": "<->", "\u2283": "=>", "\u2261": "==", "\u22a5": "_|_",
    "\u22a4": "T", "\u22a2": "|-", "\u22a8": "|=", "\u2234": ".:.",
    "\u2235": ":.:",
}
# compact alias -> char, longest first for tokenising
LOGIC_BY_ALIAS = {v: k for k, v in LOGIC_BY_CHAR.items()}
ALIASES_SORTED = sorted(LOGIC_BY_ALIAS, key=len, reverse=True)

LONG_FORMS = {
    "[NOT]": "\u00ac", "[AND]": "\u2227", "[OR]": "\u2228",
    "[IF]": "\u2192", "[IFF]": "\u2194", "[IMPLIES]": "\u2283",
    "[EQUIV]": "\u2261", "[FALSUM]": "\u22a5", "[VERUM]": "\u22a4",
    "[PROVES]": "\u22a2", "[ENTAILS]": "\u22a8",
    "[THEREFORE]": "\u2234", "[BECAUSE]": "\u2235",
    "[CIRCLED-PLUS]": "\u2295", "[XOR]": "\u22bb",
    "[SHEFFER]": "\u2191", "[NOT-PROVES]": "\u22ac",
    "[NOT-ENTAILS]": "\u22ad",
    "[SP]": " ", "[LF]": "\n", "[CR]": "\r", "[CRLF]": "\r\n",
}
LONG_BY_CHAR = {v: k for k, v in LONG_FORMS.items() if len(v) == 1 and k in
                ("[NOT]", "[AND]", "[OR]", "[IF]", "[IFF]", "[IMPLIES]",
                 "[EQUIV]", "[FALSUM]", "[VERUM]", "[PROVES]", "[ENTAILS]",
                 "[THEREFORE]", "[BECAUSE]", "[CIRCLED-PLUS]", "[XOR]",
                 "[SHEFFER]", "[NOT-PROVES]", "[NOT-ENTAILS]")}


def _check_cp(cp, abstract_surrogates=False):
    if cp > 0x10FFFF:
        raise ValueError("code point U+%X out of range (> U+10FFFF)" % cp)
    if 0xD800 <= cp <= 0xDFFF:
        if abstract_surrogates:
            return cp
        raise ValueError("surrogate U+%04X is not a valid scalar value" % cp)
    return cp


def is_surrogate_cp(cp):
    return 0xD800 <= cp <= 0xDFFF


def surrogate_token(cp):
    """Abstract reference for a surrogate code point: plain ASCII,
    same in both forms. Never a character."""
    if not is_surrogate_cp(cp):
        raise ValueError("U+%04X is not a surrogate" % cp)
    return "[SURROGATE U+%04X]" % cp


_SURROGATE_TOKEN_RE = re.compile(r"\[SURROGATE U\+([0-9A-Fa-f]{4})\]")


def _check_char(ch, abstract_surrogates=False):
    cp = ord(ch)
    _check_cp(cp, abstract_surrogates=abstract_surrogates)
    return cp


def esc_form(cp):
    """Canonical ESC form as a str (contains a real ESC byte)."""
    _check_cp(cp)
    if cp <= 0xFFFF:
        return ESC + "[U%04Xm" % cp
    return ESC + "[U%06Xm" % cp


def esc_transcription(cp):
    """Visible transcription of the ESC form, for CSVs / display."""
    _check_cp(cp)
    if cp <= 0xFFFF:
        return "<ESC>[U%04Xm" % cp
    return "<ESC>[U%06Xm" % cp


def visible_form(cp):
    _check_cp(cp)
    if cp <= 0xFFFF:
        return "\\u%04X" % cp
    return "\\U%08X" % cp


def encode_char(ch, abstract_surrogates=False):
    """Named form of one character: (esc, visible). Always encoded,
    including space / LF / CR — this is the 'named as a code point' form.
    With abstract_surrogates=True, a surrogate yields its abstract
    token in both positions: (token, token)."""
    cp = _check_char(ch, abstract_surrogates=abstract_surrogates)
    if is_surrogate_cp(cp):
        token = surrogate_token(cp)
        return token, token
    return esc_form(cp), visible_form(cp)


# ---------------------------------------------------------------- encode
def encode_text(text, form="esc", preserve_newlines=True, logic=False,
                logic_long=False, mode="both", abstract_surrogates=False):
    if mode == "esc-only" and form != "esc":
        raise ValueError("--mode esc-only: only --form esc is allowed")
    if mode == "visible-only" and form != "visible":
        raise ValueError("--mode visible-only: only --form visible is allowed")
    out = []
    i = 0
    while i < len(text):
        ch = text[i]
        cp = ord(ch)
        # A valid surrogate pair is one astral character in UTF-16
        # spelling: high (D800-DBFF) at once followed by low (DC00-DFFF).
        # Combine it and encode the astral character, in both modes.
        if 0xD800 <= cp <= 0xDBFF and i + 1 < len(text):
            lo = ord(text[i + 1])
            if 0xDC00 <= lo <= 0xDFFF:
                astral = 0x10000 + (cp - 0xD800) * 0x400 + (lo - 0xDC00)
                out.append(esc_form(astral) if form == "esc"
                           else visible_form(astral))
                i += 2
                continue
        _check_char(ch, abstract_surrogates=abstract_surrogates)
        if is_surrogate_cp(cp):
            out.append(surrogate_token(cp))
            i += 1
            continue
        if logic and ch in LOGIC_BY_CHAR:
            out.append(LOGIC_BY_CHAR[ch])
        elif logic_long and ch in LONG_BY_CHAR:
            out.append(LONG_BY_CHAR[ch])
        elif ch == "\n" and preserve_newlines:
            out.append("\n")
        elif 0x20 <= cp <= 0x7E:
            if form == "visible" and ch == "\\":
                out.append("\\\\")
            else:
                out.append(ch)
        else:
            # control or non-ASCII: encode
            out.append(esc_form(cp) if form == "esc" else visible_form(cp))
        i += 1
    return "".join(out)


# ---------------------------------------------------------------- decode
_ESC_RE = re.compile(r"\x1b\[U([0-9A-Fa-f]{4}|[0-9A-Fa-f]{6})m")


def decode_esc(data, abstract_surrogates=False):
    """Decode ESC-form bytes (or str) to text. Literal ASCII passes
    through; any ESC not starting a valid ESC[U....m sequence is an error.
    With abstract_surrogates=True, an ESC surrogate form yields the
    abstract token, never a lone surrogate character."""
    if isinstance(data, str):
        raw = data.encode("ascii", "strict")
    else:
        raw = bytes(data)
    # validate all bytes are ASCII
    for b in raw:
        if b > 0x7F:
            raise ValueError("non-ASCII byte 0x%02X in ESC-form input" % b)
    text = raw.decode("ascii")
    out = []
    i = 0
    while i < len(text):
        if text[i] == ESC:
            m = _ESC_RE.match(text, i)
            if not m:
                raise ValueError("malformed ESC sequence at offset %d: %r"
                                 % (i, text[i:i + 12]))
            cp = int(m.group(1), 16)
            if len(m.group(1)) == 4 and cp > 0xFFFF:
                raise ValueError("4-digit ESC form with value > U+FFFF at %d" % i)
            _check_cp(cp, abstract_surrogates=abstract_surrogates)
            if is_surrogate_cp(cp):
                out.append(surrogate_token(cp))
            else:
                out.append(chr(cp))
            i = m.end()
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def decode_visible(text, aliases=False, logic=False,
                   abstract_surrogates=False):
    """Decode visible-form text. Handles \\uXXXX, \\UXXXXXXXX, \\\\.
    Aliases ([SP] etc. and logic long forms) only with aliases=True.
    Compact logic aliases only with logic=True (formula mode).
    With abstract_surrogates=True, a \\u/\\U surrogate form and the
    [SURROGATE U+XXXX] token both yield that abstract token, never
    a lone surrogate character."""
    out = []
    i = 0
    while i < len(text):
        ch = text[i]
        if abstract_surrogates and ch == "[":
            m = _SURROGATE_TOKEN_RE.match(text, i)
            if m:
                cp = int(m.group(1), 16)
                if is_surrogate_cp(cp):
                    out.append(surrogate_token(cp))
                    i = m.end()
                    continue
                raise ValueError("surrogate token with non-surrogate "
                                 "code point at offset %d: %r" % (i, m.group(0)))
        if ch == "\\" and i + 1 < len(text):
            nxt = text[i + 1]
            if nxt == "\\":
                out.append("\\")
                i += 2
                continue
            if nxt == "u":
                hexpart = text[i + 2:i + 6]
                if len(hexpart) != 4 or not all(c in "0123456789ABCDEFabcdef" for c in hexpart):
                    raise ValueError("malformed \\u escape at offset %d: %r"
                                     % (i, text[i:i + 8]))
                cp = int(hexpart, 16)
                _check_cp(cp, abstract_surrogates=abstract_surrogates)
                if is_surrogate_cp(cp):
                    out.append(surrogate_token(cp))
                else:
                    out.append(chr(cp))
                i += 6
                continue
            if nxt == "U":
                hexpart = text[i + 2:i + 10]
                if len(hexpart) != 8 or not all(c in "0123456789ABCDEFabcdef" for c in hexpart):
                    raise ValueError("malformed \\U escape at offset %d: %r"
                                     % (i, text[i:i + 12]))
                cp = int(hexpart, 16)
                _check_cp(cp, abstract_surrogates=abstract_surrogates)
                if is_surrogate_cp(cp):
                    out.append(surrogate_token(cp))
                else:
                    out.append(chr(cp))
                i += 10
                continue
            # unknown backslash sequence: leave literal
            out.append(ch)
            i += 1
            continue
        if aliases and ch == "[":
            matched = False
            for token, val in LONG_FORMS.items():
                if text.startswith(token, i):
                    out.append(val)
                    i += len(token)
                    matched = True
                    break
            if matched:
                continue
        if logic:
            matched = False
            for alias in ALIASES_SORTED:
                if text.startswith(alias, i):
                    # 'T' and single-char aliases are only taken when the
                    # alias is a whole token in formula mode; for the
                    # single-char aliases ~ & | T, require that the next
                    # char is not alphanumeric (so 'Tom' is not ⊤om).
                    if len(alias) == 1 and i + 1 < len(text) and text[i + 1].isalnum():
                        continue
                    out.append(LOGIC_BY_ALIAS[alias])
                    i += len(alias)
                    matched = True
                    break
            if matched:
                continue
        out.append(ch)
        i += 1
    return "".join(out)


def decode_text(data, form="auto", aliases=False, logic=False, mode="both",
                abstract_surrogates=False):
    """Decode encoded input. form: esc | visible | auto (both modes only).
    In esc-only mode, visible escapes are left literal. In visible-only
    mode, a literal ESC byte is an error."""
    if mode == "esc-only":
        if isinstance(data, str):
            data = data.encode("ascii")
        return decode_esc(data, abstract_surrogates=abstract_surrogates)
    if mode == "visible-only":
        if isinstance(data, bytes):
            if b"\x1b" in data:
                raise ValueError("literal ESC byte in visible-only input")
            data = data.decode("ascii")
        return decode_visible(data, aliases=aliases, logic=logic,
                              abstract_surrogates=abstract_surrogates)
    # both
    if form == "esc":
        return decode_esc(data, abstract_surrogates=abstract_surrogates)
    if form == "visible":
        if isinstance(data, bytes):
            data = data.decode("ascii")
        return decode_visible(data, aliases=aliases, logic=logic,
                              abstract_surrogates=abstract_surrogates)
    # auto: bytes containing ESC -> decode ESC sequences, then decode
    # any visible escapes in the remaining literal text.
    if isinstance(data, str):
        data = data.encode("ascii")
    intermediate = decode_esc(data, abstract_surrogates=abstract_surrogates)
    return decode_visible(intermediate, aliases=aliases, logic=logic,
                          abstract_surrogates=abstract_surrogates)


# ---------------------------------------------------------------- convert
def convert_esc_to_visible(data, aliases=False, abstract_surrogates=False):
    """ESC-form bytes -> visible-form text (lossless, token by token).
    A literal LF in the input stays a literal LF; an encoded LF
    (ESC[U000Am) stays encoded (\\u000A). A literal backslash
    becomes '\\\\' in the visible form. This preserves byte-level
    round-trips: ESC -> visible -> ESC is identical.
    With abstract_surrogates=True, an ESC surrogate form becomes
    the abstract token [SURROGATE U+XXXX]; without it, it is rejected."""
    if isinstance(data, str):
        data = data.encode("ascii")
    text = data.decode("ascii")
    out = []
    i = 0
    while i < len(text):
        if text[i] == ESC:
            m = _ESC_RE.match(text, i)
            if not m:
                raise ValueError("malformed ESC sequence at offset %d: %r"
                                 % (i, text[i:i + 12]))
            cp = int(m.group(1), 16)
            _check_cp(cp, abstract_surrogates=abstract_surrogates)
            if is_surrogate_cp(cp):
                out.append(surrogate_token(cp))
            else:
                out.append(visible_form(cp))
            i = m.end()
        elif text[i] == "\\":
            out.append("\\\\")
            i += 1
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def convert_visible_to_esc(text, aliases=False, abstract_surrogates=False):
    """Visible-form text -> ESC-form bytes (lossless, token by token).
    A literal LF stays a literal LF; an encoded LF (\\u000A) stays
    encoded (ESC[U000Am). '\\\\' becomes a literal backslash.
    With abstract_surrogates=True, a \\u/\\U surrogate form and the
    [SURROGATE U+XXXX] token both become that abstract token;
    without it, they are rejected."""
    if isinstance(text, bytes):
        text = text.decode("ascii")
    out = []
    i = 0
    while i < len(text):
        ch = text[i]
        if abstract_surrogates and ch == "[":
            m = _SURROGATE_TOKEN_RE.match(text, i)
            if m:
                cp = int(m.group(1), 16)
                if is_surrogate_cp(cp):
                    out.append(surrogate_token(cp))
                    i = m.end()
                    continue
                raise ValueError("surrogate token with non-surrogate "
                                 "code point at offset %d: %r" % (i, m.group(0)))
        if ch == "\\" and i + 1 < len(text):
            nxt = text[i + 1]
            if nxt == "\\":
                out.append("\\")
                i += 2
                continue
            if nxt == "u":
                hexpart = text[i + 2:i + 6]
                if len(hexpart) != 4 or not all(c in "0123456789ABCDEFabcdef" for c in hexpart):
                    raise ValueError("malformed \\u escape at offset %d" % i)
                cp = int(hexpart, 16)
                _check_cp(cp, abstract_surrogates=abstract_surrogates)
                if is_surrogate_cp(cp):
                    out.append(surrogate_token(cp))
                else:
                    out.append(esc_form(cp))
                i += 6
                continue
            if nxt == "U":
                hexpart = text[i + 2:i + 10]
                if len(hexpart) != 8 or not all(c in "0123456789ABCDEFabcdef" for c in hexpart):
                    raise ValueError("malformed \\U escape at offset %d" % i)
                cp = int(hexpart, 16)
                _check_cp(cp, abstract_surrogates=abstract_surrogates)
                if is_surrogate_cp(cp):
                    out.append(surrogate_token(cp))
                else:
                    out.append(esc_form(cp))
                i += 10
                continue
            out.append(ch)
            i += 1
            continue
        if aliases and ch == "[":
            matched = False
            for token, val in LONG_FORMS.items():
                if text.startswith(token, i):
                    for vch in val:
                        out.append(esc_form(ord(vch)) if ord(vch) not in (0x0A,) else "\n")
                    i += len(token)
                    matched = True
                    break
            if matched:
                continue
        out.append(ch)
        i += 1
    return "".join(out).encode("ascii")


def convert(data, to="visible", mode="both", aliases=False,
            abstract_surrogates=False):
    if mode == "esc-only" and to == "visible":
        raise ValueError("--mode esc-only: convert --to visible is not allowed")
    if mode == "visible-only" and to == "esc":
        raise ValueError("--mode visible-only: convert --to esc is not allowed")
    if to == "visible":
        if isinstance(data, str):
            data = data.encode("ascii")
        return convert_esc_to_visible(data, aliases=aliases,
                                      abstract_surrogates=abstract_surrogates).encode("ascii")
    if isinstance(data, bytes):
        data = data.decode("ascii")
    return convert_visible_to_esc(data, aliases=aliases,
                                  abstract_surrogates=abstract_surrogates)


# ---------------------------------------------------------------- CLI
def _read_input(args):
    if args.input is None:
        data = sys.stdin.buffer.read()
        return data
    with open(args.input, "rb") as f:
        return f.read()


def _write_output(args, data):
    if isinstance(data, str):
        data = data.encode("utf-8" if args.output_text else "ascii", "replace")
    if args.output:
        with open(args.output, "wb") as f:
            f.write(data)
    else:
        sys.stdout.buffer.write(data)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="ASCII/ANSI code for Unicode + sentential logic "
                    "(Unicode %s, code v%s)" % (UNICODE_VERSION, VERSION))
    p.add_argument("--mode", choices=["both", "esc-only", "visible-only"],
                   default="both", help="variant: both (default), esc-only, visible-only")
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("encode", help="UTF-8 text -> encoded form")
    pe.add_argument("input", nargs="?", help="input UTF-8 file (default: stdin)")
    pe.add_argument("--form", choices=["esc", "visible"], default="esc")
    pe.add_argument("--output", help="output file (default: stdout)")
    pe.add_argument("--preserve-newlines", dest="preserve_newlines",
                    action="store_true", default=True)
    pe.add_argument("--no-preserve-newlines", dest="preserve_newlines",
                    action="store_false")
    pe.add_argument("--logic", action="store_true",
                    help="opt-in: logic chars -> compact aliases")
    pe.add_argument("--logic-long", action="store_true",
                    help="opt-in: logic chars -> long forms [NOT] etc.")
    pe.add_argument("--abstract-surrogates", action="store_true",
                    help="opt-in: lone surrogates -> abstract token "
                         "[SURROGATE U+XXXX]; input read with "
                         "errors='surrogatepass'")
    pe.add_argument("--output-text", action="store_true", default=False)

    pd = sub.add_parser("decode", help="encoded form -> UTF-8 text")
    pd.add_argument("input", nargs="?", help="input file (default: stdin)")
    pd.add_argument("--form", choices=["esc", "visible", "auto"], default="auto")
    pd.add_argument("--output", help="output file (default: stdout)")
    pd.add_argument("--aliases", action="store_true",
                    help="decode [SP]/[LF]/[CR]/[CRLF] and logic long forms")
    pd.add_argument("--logic", action="store_true",
                    help="opt-in formula mode: compact aliases -> logic chars")
    pd.add_argument("--abstract-surrogates", action="store_true",
                    help="opt-in: surrogate forms / tokens -> abstract token "
                         "[SURROGATE U+XXXX], never a lone surrogate character")
    pd.add_argument("--output-text", action="store_true", default=True)

    pc = sub.add_parser("convert", help="ESC form <-> visible form, lossless")
    pc.add_argument("input", nargs="?", help="input file (default: stdin)")
    pc.add_argument("--to", choices=["esc", "visible"], required=True)
    pc.add_argument("--output", help="output file (default: stdout)")
    pc.add_argument("--aliases", action="store_true")
    pc.add_argument("--abstract-surrogates", action="store_true",
                    help="opt-in: surrogate forms -> abstract token "
                         "[SURROGATE U+XXXX]")
    pc.add_argument("--output-text", action="store_true", default=False)

    args = p.parse_args(argv)
    data = _read_input(args)

    if args.cmd == "encode":
        text = data.decode("utf-8", errors="surrogatepass"
                           if args.abstract_surrogates else "strict")
        out = encode_text(text, form=args.form,
                          preserve_newlines=args.preserve_newlines,
                          logic=args.logic, logic_long=args.logic_long,
                          mode=args.mode,
                          abstract_surrogates=args.abstract_surrogates)
        _write_output(args, out.encode("ascii"))
    elif args.cmd == "decode":
        out = decode_text(data, form=args.form, aliases=args.aliases,
                          logic=args.logic, mode=args.mode,
                          abstract_surrogates=args.abstract_surrogates)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(out)
        else:
            sys.stdout.buffer.write(out.encode("utf-8"))
    elif args.cmd == "convert":
        out = convert(data, to=args.to, mode=args.mode, aliases=args.aliases,
                      abstract_surrogates=args.abstract_surrogates)
        _write_output(args, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
