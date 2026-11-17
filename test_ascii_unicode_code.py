#!/usr/bin/env python3
"""Test harness for ascii_unicode_code.py. Run: python3 test_ascii_unicode_code.py
Prints counts; exits non-zero if any test fails. Results are recorded in
TEST_REPORT.md (generated from the printed output of the actual run)."""
import sys
import unicodedata

sys.path.insert(0, ".")
from ascii_unicode_code import (
    encode_text, decode_text, decode_esc, decode_visible,
    convert_esc_to_visible, convert_visible_to_esc,
    esc_form, visible_form, encode_char, UNICODE_VERSION,
)
from generate_mapping import parse_ucd, TOTAL

results = {}


def check(name, passed, failed):
    results[name] = (passed, failed)
    print("%s: pass=%d fail=%d" % (name, passed, failed))
    return failed == 0


def main():
    ok = True
    assigned = parse_ucd("UnicodeData.txt")
    assigned_cps = sorted(assigned.keys())
    # (a) all assigned characters, ESC + visible, in chunks of 8192
    for form in ("esc", "visible"):
        passed = failed = 0
        for i in range(0, len(assigned_cps), 8192):
            chunk = "".join(chr(cp) for cp in assigned_cps[i:i + 8192])
            try:
                enc = encode_text(chunk, form=form, preserve_newlines=False)
                dec = decode_text(enc.encode("ascii"), form=form)
                if dec == chunk:
                    passed += len(chunk)
                else:
                    failed += len(chunk)
            except Exception as e:
                print("assigned %s chunk %d error: %s" % (form, i, e))
                failed += len(chunk)
        ok &= check("assigned_roundtrip_%s" % form, passed, failed)

    # (b) all 1,114,112 code points where applicable: every scalar value
    # (all except surrogates U+D800-U+DFFF). Encoded in chunks of 8192.
    # Noncharacters / private-use / unassigned are valid scalar values
    # and must round-trip as characters; only surrogates are excluded.
    for form in ("esc", "visible"):
        passed = failed = 0
        scalar = [cp for cp in range(TOTAL) if not (0xD800 <= cp <= 0xDFFF)]
        for i in range(0, len(scalar), 8192):
            chunk = "".join(chr(cp) for cp in scalar[i:i + 8192])
            try:
                enc = encode_text(chunk, form=form, preserve_newlines=False)
                # encoded output must be ASCII-only
                assert max(enc.encode("ascii")) <= 0x7F
                dec = decode_text(enc.encode("ascii"), form=form)
                if dec == chunk:
                    passed += len(chunk)
                else:
                    failed += len(chunk)
            except Exception as e:
                print("all_scalar %s chunk %d error: %s" % (form, i, e))
                failed += len(chunk)
        ok &= check("all_scalar_roundtrip_%s" % form, passed, failed)
        print("  scalar values tested: %d" % len(scalar))

    # (c) logic inventory
    from generate_mapping import LOGIC
    passed = failed = 0
    for sym, cp, alias, longf in LOGIC:
        try:
            e, v = encode_char(sym)
            assert decode_esc(e.encode("ascii")) == sym
            assert decode_visible(v) == sym
            assert visible_form(cp) == v
            # compact alias round-trip in formula mode (skip no-alias rows)
            if alias:
                enc = encode_text(sym, form="visible", logic=True)
                assert enc == alias, (enc, alias)
                dec = decode_visible(enc, logic=True)
                assert dec == sym, (dec, sym)
            passed += 1
        except Exception as e:
            print("logic %U+%04X error: %s" % (cp, e))
            failed += 1
    ok &= check("logic_inventory", passed, failed)

    # (d) space / LF / CR / CRLF
    passed = failed = 0
    cases = [
        (" ", "space literal"),
        ("\n", "LF literal, preserve_newlines"),
        ("\r", "CR encoded"),
        ("\r\n", "CRLF"),
        ("a b\nc\rd\r\ne", "mixed"),
    ]
    for text, label in cases:
        try:
            for form in ("esc", "visible"):
                enc = encode_text(text, form=form, preserve_newlines=True)
                dec = decode_text(enc.encode("ascii"), form=form)
                assert dec == text, (label, form, repr(dec))
            # named forms
            for ch in (" ", "\n", "\r"):
                e, v = encode_char(ch)
                assert decode_esc(e.encode("ascii")) == ch
                assert decode_visible(v) == ch
            # aliases, visible, opt-in
            assert decode_visible("[SP][LF][CR][CRLF]", aliases=True) == " \n\r\r\n"
            passed += 1
        except Exception as e:
            print("space/newline %s error: %s" % (label, e))
            failed += 1
    ok &= check("space_lf_cr_crlf", passed, failed)

    # (e) ESC <-> visible conversion both ways, on a mixed sample
    passed = failed = 0
    sample = "".join(chr(cp) for cp in
                     [0x41, 0x20, 0x00AC, 0x2227, 0x2192, 0x1F600, 0x4E2D, 0x10FFFF, 0x0001, 0x007F])
    try:
        esc = encode_text(sample, form="esc", preserve_newlines=False).encode("ascii")
        vis = convert_esc_to_visible(esc)
        back = convert_visible_to_esc(vis)
        assert back == esc, (back, esc)
        assert decode_visible(vis) == sample
        assert decode_esc(back) == sample
        passed += 1
    except Exception as e:
        print("convert sample error: %s" % e)
        failed += 1
    # conversion on all assigned characters, chunked
    try:
        p2 = f2 = 0
        for i in range(0, len(assigned_cps), 8192):
            chunk = "".join(chr(cp) for cp in assigned_cps[i:i + 8192])
            esc = encode_text(chunk, form="esc", preserve_newlines=False).encode("ascii")
            vis = convert_esc_to_visible(esc)
            back = convert_visible_to_esc(vis)
            if back == esc:
                p2 += len(chunk)
            else:
                f2 += len(chunk)
        passed += p2
        failed += f2
    except Exception as e:
        print("convert assigned error: %s" % e)
        failed += len(assigned_cps)
    ok &= check("esc_visible_conversion", passed, failed)

    # (f) negative tests
    neg = [
        ("surrogate encode", lambda: encode_text("\ud800", form="esc")),
        ("surrogate decode visible", lambda: decode_visible("\\uD800")),
        ("surrogate decode esc", lambda: decode_esc(b"\x1b[UD800m")),
        ("out-of-range decode esc", lambda: decode_esc(b"\x1b[U110000m")),
        ("out-of-range decode visible", lambda: decode_visible("\\U00110000")),
        ("malformed ESC hex", lambda: decode_esc(b"\x1b[U00ZZm")),
        ("malformed ESC no terminator", lambda: decode_esc(b"\x1b[U00AC")),
        ("malformed \\u short", lambda: decode_visible("\\u00")),
        ("malformed \\U short", lambda: decode_visible("\\U0001F6")),
        ("non-ASCII byte in ESC input", lambda: decode_esc(b"\x1b[U00ACm\xc3\xa9")),
        ("esc-only rejects visible form", lambda: encode_text("x", form="visible", mode="esc-only")),
        ("visible-only rejects esc form", lambda: encode_text("x", form="esc", mode="visible-only")),
    ]
    passed = failed = 0
    for label, fn in neg:
        try:
            fn()
            print("NEGATIVE FAIL (no error raised): %s" % label)
            failed += 1
        except (ValueError, UnicodeEncodeError, UnicodeDecodeError):
            passed += 1
        except Exception as e:
            print("NEGATIVE wrong exception %s: %r" % (label, e))
            failed += 1
    ok &= check("negative_tests", passed, failed)

    # (g) abstract surrogate mode, opt-in only
    passed = failed = 0
    try:
        # all 2,048 surrogates: encode -> token, decode token/forms -> token
        for cp in range(0xD800, 0xE000):
            ch = chr(cp)
            token = "[SURROGATE U+%04X]" % cp
            e, v = encode_char(ch, abstract_surrogates=True)
            assert e == v == token, (cp, e, v)
            assert encode_text(ch, form="visible",
                               abstract_surrogates=True) == token
            assert encode_text(ch, form="esc",
                               abstract_surrogates=True) == token
            assert decode_visible(v, abstract_surrogates=True) == token
            assert decode_visible(token, abstract_surrogates=True) == token
            assert decode_esc(e.encode("ascii"),
                              abstract_surrogates=True) == token
            assert convert_esc_to_visible(e.encode("ascii"),
                                          abstract_surrogates=True) == token
            assert convert_visible_to_esc(v,
                                          abstract_surrogates=True) == token.encode("ascii")
            passed += 1
        # mixed text, both forms, token stays valid ASCII
        mixed = "a\ud800b\udfff"
        enc = encode_text(mixed, form="visible", abstract_surrogates=True)
        assert enc == "a[SURROGATE U+D800]b[SURROGATE U+DFFF]", enc
        assert max(enc.encode("ascii")) <= 0x7F
        dec = decode_text(enc.encode("ascii"), form="visible",
                          abstract_surrogates=True)
        assert dec == enc, (dec, enc)
        # default mode still rejects (also covered by negative tests)
        for fn in (lambda: encode_text("\ud800", form="visible"),
                   lambda: decode_visible("\\uD800"),
                   lambda: decode_esc(b"\x1b[UD800m"),
                   lambda: convert_esc_to_visible(b"\x1b[UD800m"),
                   lambda: convert_visible_to_esc("\\uD800")):
            try:
                fn()
                raise AssertionError("default mode accepted a surrogate")
            except ValueError:
                pass
        passed += 1
    except Exception as e:
        print("abstract surrogates error: %s" % e)
        failed += 1
    ok &= check("abstract_surrogates", passed, failed)

    # (g2) surrogate pairs are one astral character, in both modes
    passed = failed = 0
    try:
        pair = "\ud83d\ude00"  # UTF-16 pair for U+1F600
        for form in ("esc", "visible"):
            for flag in (False, True):
                enc = encode_text(pair, form=form,
                                  abstract_surrogates=flag)
                dec = decode_text(enc.encode("ascii"), form=form,
                                  abstract_surrogates=flag)
                assert dec == "\U0001F600", (form, flag, enc, dec)
        assert encode_text(pair, form="visible") == "\\U0001F600"
        assert encode_text(pair + "\ud800", form="visible",
                           abstract_surrogates=True) == \
            "\\U0001F600[SURROGATE U+D800]"
        # lone / mismatched surrogates are not pairs
        for bad in ("\ud800", "\udc00", "\ud800\ud800", "\udc00\ud800"):
            try:
                encode_text(bad, form="visible")
                raise AssertionError("default mode accepted %r" % bad)
            except ValueError:
                pass
            assert encode_text(bad, form="visible",
                               abstract_surrogates=True) == "".join(
                "[SURROGATE U+%04X]" % ord(c) for c in bad)
        passed += 1
    except Exception as e:
        print("surrogate pairs error: %s" % e)
        failed += 1
    ok &= check("surrogate_pairs", passed, failed)

    # variant spot checks: esc-only and visible-only round-trips
    for mode, form in (("esc-only", "esc"), ("visible-only", "visible")):
        passed = failed = 0
        sample2 = "".join(chr(cp) for cp in [0x41, 0x20, 0x00AC, 0x2227, 0x1F600, 0x4E2D])
        try:
            enc = encode_text(sample2, form=form, preserve_newlines=False, mode=mode)
            dec = decode_text(enc.encode("ascii"), form=form, mode=mode)
            assert dec == sample2
            passed += 1
        except Exception as e:
            print("variant %s error: %s" % (mode, e))
            failed += 1
        # logic inventory in each variant
        try:
            for sym, cp, alias, longf in LOGIC:
                enc = encode_text(sym, form=form, preserve_newlines=False, mode=mode)
                assert decode_text(enc.encode("ascii"), form=form, mode=mode) == sym
            passed += len(LOGIC)
        except Exception as e:
            print("variant %s logic error: %s" % (mode, e))
            failed += len(LOGIC)
        ok &= check("variant_%s" % mode, passed, failed)

    print("Python %s, unicodedata %s, UnicodeData %s, assigned=%d"
          % (sys.version.split()[0], unicodedata.unidata_version,
             UNICODE_VERSION, len(assigned_cps)))
    print("OVERALL: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
