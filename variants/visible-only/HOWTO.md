# How-to — visible-only variant

Run all commands from inside this folder:

```bash
cd ~/workspace/ascii-unicode-code/variants/visible-only
```

No installation. Python 3.8 or later, no dependencies.

## 1. Encode a sentence

```bash
printf 'Hello, \xe4\xb8\x96\xe7\x95\x8c! \xf0\x9f\x98\x80\n' > /tmp/hello.txt
python3 ascii_unicode_code.py --mode visible-only encode --form visible /tmp/hello.txt
```

Expected output:

```
Hello, \u4E16\u754C! \U0001F600
```

## 2. Decode it back

```bash
python3 ascii_unicode_code.py --mode visible-only encode --form visible /tmp/hello.txt > /tmp/hello.vis
python3 ascii_unicode_code.py --mode visible-only decode --form visible /tmp/hello.vis
```

Expected output: `Hello, 世界! 😀`.

## 3. Encode a logic formula

```bash
printf '\xc2\xacp \xe2\x88\xa7 q \xe2\x86\x92 r\n' > /tmp/formula.txt
python3 ascii_unicode_code.py --mode visible-only encode --form visible /tmp/formula.txt
python3 ascii_unicode_code.py --mode visible-only encode --form visible --logic /tmp/formula.txt
```

Expected output: `\u00ACp \u2227 q \u2192 r`, then `~p & q -> r`.

Decode a compact-alias formula back:

```bash
printf '~p & q -> r\n' > /tmp/formula-ascii.txt
python3 ascii_unicode_code.py --mode visible-only decode --form visible --logic /tmp/formula-ascii.txt
```

Expected output: `¬p ∧ q → r`.

## 4. Encode space, LF, and CR

```bash
printf 'a b\nc\r\nd' > /tmp/spaces.txt
python3 ascii_unicode_code.py --mode visible-only encode --form visible /tmp/spaces.txt | od -c
```

Expected: `a`, space, `b`, a literal LF, `c`, then the
characters `\`, `u`, `0`, `0`, `0`, `D` (CR, encoded), then
a literal LF, then `d`.

Decode the readable aliases:

```bash
printf '[SP][LF][CR][CRLF]' | python3 ascii_unicode_code.py --mode visible-only decode --form visible --aliases | od -c
```

Expected bytes: space, LF, CR, CR, LF.

## 5. Look up a character

The mapping files live in the parent folder:

```bash
grep '^U+00AC,' ../../unicode_mapping.csv
grep '^U+01F600,' ../../unicode_mapping.csv
cat ../../logic_mapping.csv
```

## 6. What is an error here

```bash
python3 ascii_unicode_code.py --mode visible-only encode --form esc /tmp/hello.txt
echo "exit: $?"
python3 ascii_unicode_code.py --mode visible-only convert --to esc /tmp/hello.vis
echo "exit: $?"
```

Both should exit with code 1 and an error naming the mode
restriction. That is by design — this variant has no ESC form.
