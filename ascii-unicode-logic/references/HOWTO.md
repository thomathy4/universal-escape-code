# How-to — step-by-step tasks

Run all commands from inside `~/workspace/ascii-unicode-code`:

```bash
cd ~/workspace/ascii-unicode-code
```

No installation is needed. Python 3.8 or later, no dependencies.
Tested with Python 3.12.3.

## 1. Encode a sentence

Goal: turn a UTF-8 sentence into the visible form.

```bash
printf 'Hello, \xe4\xb8\x96\xe7\x95\x8c! \xf0\x9f\x98\x80\n' > /tmp/hello.txt
python3 ascii_unicode_code.py encode --form visible /tmp/hello.txt
```

Expected output:

```
Hello, \u4E16\u754C! \U0001F600
```

What happened: `世界` became `\u4E16\u754C` and `😀` became
`\U0001F600`. `Hello, `, `!` and the space stayed literal.
The trailing newline stayed literal too (see task 5).

To encode to the ESC form instead, use `--form esc`. The
output contains real ESC bytes, so view it with `od -c`:

```bash
python3 ascii_unicode_code.py encode --form esc /tmp/hello.txt | od -c | head
```

## 2. Decode it back

Goal: turn encoded text back into the original UTF-8 text.

```bash
python3 ascii_unicode_code.py encode --form visible /tmp/hello.txt > /tmp/hello.vis
python3 ascii_unicode_code.py decode --form visible /tmp/hello.vis
```

Expected output: the original sentence, `Hello, 世界! 😀`.

For ESC form, decode with `--form esc`:

```bash
python3 ascii_unicode_code.py encode --form esc /tmp/hello.txt > /tmp/hello.esc
python3 ascii_unicode_code.py decode --form esc /tmp/hello.esc
```

If you do not know which form a file is in, use `--form auto`
(the default for `decode`): it decodes ESC sequences first,
then visible escapes.

```bash
python3 ascii_unicode_code.py decode /tmp/hello.vis
python3 ascii_unicode_code.py decode /tmp/hello.esc
```

## 3. Convert ESC form to visible form (and back)

Goal: change forms without changing the characters.

```bash
python3 ascii_unicode_code.py convert --to visible /tmp/hello.esc
```

Expected output: the visible form from task 1.

```bash
python3 ascii_unicode_code.py convert --to esc /tmp/hello.vis
```

Expected output: ESC-form bytes (view with `od -c` if you
want to see them).

To check the conversion is lossless, convert there and back
and compare:

```bash
python3 ascii_unicode_code.py convert --to visible /tmp/hello.esc > /tmp/hello.vis2
python3 ascii_unicode_code.py convert --to esc /tmp/hello.vis2 > /tmp/hello.esc2
cmp /tmp/hello.esc /tmp/hello.esc2 && echo "lossless: files are identical"
```

## 4. Encode a logic formula

Goal: encode a sentential-logic formula three ways.

First, write the formula. The `printf` line below writes
the UTF-8 bytes for `¬p ∧ q → r` followed by a newline:

```bash
printf '\xc2\xacp \xe2\x88\xa7 q \xe2\x86\x92 r\n' > /tmp/formula.txt
```

Canonical visible form:

```bash
python3 ascii_unicode_code.py encode --form visible /tmp/formula.txt
```

Expected output:

```
\u00ACp \u2227 q \u2192 r
```

Compact aliases (opt-in, `--logic`):

```bash
python3 ascii_unicode_code.py encode --form visible --logic /tmp/formula.txt
```

Expected output:

```
~p & q -> r
```

Decode a compact-alias formula back (formula mode only —
do not use `--logic` on general text):

```bash
printf '~p & q -> r\n' > /tmp/formula-ascii.txt
python3 ascii_unicode_code.py decode --form visible --logic /tmp/formula-ascii.txt
```

Expected output: `¬p ∧ q → r`.

Long forms (visible form only, opt-in on decode with
`--aliases`):

```bash
printf '[NOT]p [AND] q [IF] r\n' > /tmp/formula-long.txt
python3 ascii_unicode_code.py decode --form visible --aliases /tmp/formula-long.txt
```

Expected output: `¬p ∧ q → r`.

## 5. Encode space, LF, and CR

Goal: see how space, line feed, and carriage return are handled.

Write a file containing `a b`, a line feed, `c`, a carriage
return + line feed, and `d`:

```bash
printf 'a b\nc\r\nd' > /tmp/spaces.txt
python3 ascii_unicode_code.py encode --form visible /tmp/spaces.txt | od -c
```

Expected: `a`, space, `b`, a literal LF, `c`, then the
characters `\`, `u`, `0`, `0`, `0`, `D` (the visible form of
CR), then a literal LF, then `d`. The space and the LFs stay
literal; the CR is encoded.

To encode the LF as well, add `--no-preserve-newlines`:

```bash
python3 ascii_unicode_code.py encode --form visible --no-preserve-newlines /tmp/spaces.txt
```

To name a character as a code point (always encoded):

```bash
python3 -c "from ascii_unicode_code import encode_char; print(encode_char(' ')); print(encode_char(chr(10))); print(encode_char(chr(13)))"
```

Expected output (the ESC form is shown with a real ESC byte,
so it may look odd in a terminal — the visible form is the
second item in each pair):

```
('\x1b[U0020m', '\\u0020')
('\x1b[U000Am', '\\u000A')
('\x1b[U000Dm', '\\u000D')
```

To decode the readable aliases `[SP]`, `[LF]`, `[CR]`,
`[CRLF]`:

```bash
printf '[SP][LF][CR][CRLF]' | python3 ascii_unicode_code.py decode --form visible --aliases | od -c
```

Expected bytes: space, LF, CR, CR, LF.

## 6. Look up a character in the mapping

Goal: find a character's name, status, and forms.

```bash
grep '^U+00AC,' unicode_mapping.csv
grep '^U+01F600,' unicode_mapping.csv
grep '^U+0020,' unicode_mapping.csv
```

Expected output:

```
U+00AC,172,NOT SIGN,assigned,<ESC>[U00ACm,\u00AC,~
U+01F600,128512,GRINNING FACE,assigned,<ESC>[U01F600m,\U0001F600,
U+0020,32,SPACE,assigned,<ESC>[U0020m,\u0020,
```

Columns: codepoint, decimal, Unicode name, status, ESC form
(as `<ESC>…`), visible form, logic alias (empty unless the
character is a logic symbol).

To see the whole logic inventory:

```bash
cat logic_mapping.csv
```

To count the rows:

```bash
wc -l unicode_mapping.csv logic_mapping.csv
```

Expected: 1,114,113 lines in `unicode_mapping.csv` (1 header
+ 1,114,112 code points) and 19 lines in `logic_mapping.csv`
(1 header + 18 symbols).

## 7. Run the tests yourself

```bash
python3 test_ascii_unicode_code.py
```

Expected last line: `OVERALL: PASS`. The full counts are
in `TEST_REPORT.md`.

## 8. Use a single-form variant

Goal: use only one form.

ESC-only:

```bash
cd variants/esc-only
python3 ascii_unicode_code.py --mode esc-only encode --form esc /tmp/hello.txt | od -c | head
```

Visible-only:

```bash
cd ../visible-only
python3 ascii_unicode_code.py --mode visible-only encode --form visible /tmp/hello.txt
```

(Each variant folder has its own `README.md` and
`VARIANT.md`. The mapping CSVs live in the parent folder
and are shared — they are not copied into the variant
folders.)
