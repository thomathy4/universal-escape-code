# How-to — ESC-only variant

Run all commands from inside this folder:

```bash
cd ~/workspace/ascii-unicode-code/variants/esc-only
```

No installation. Python 3.8 or later, no dependencies.

## 1. Encode a sentence

```bash
printf 'Hello, \xe4\xb8\x96\xe7\x95\x8c! \xf0\x9f\x98\x80\n' > /tmp/hello.txt
python3 ascii_unicode_code.py --mode esc-only encode --form esc /tmp/hello.txt | od -c | head
```

`od -c` is used because the output contains real ESC bytes.
You should see `033 [ U 4 E 1 6 m` (for U+4E16) and
`033 [ U 0 1 F 6 0 0 m` (for U+1F600) among the literal
ASCII characters.

## 2. Decode it back

```bash
python3 ascii_unicode_code.py --mode esc-only encode --form esc /tmp/hello.txt > /tmp/hello.esc
python3 ascii_unicode_code.py --mode esc-only decode --form esc /tmp/hello.esc
```

Expected output: `Hello, 世界! 😀`.

## 3. Encode a logic formula

```bash
printf '\xc2\xacp \xe2\x88\xa7 q \xe2\x86\x92 r\n' > /tmp/formula.txt
python3 ascii_unicode_code.py --mode esc-only encode --form esc /tmp/formula.txt | od -c | head
python3 ascii_unicode_code.py --mode esc-only encode --form esc --logic /tmp/formula.txt
```

Expected output of the second command: `~p & q -> r`.

## 4. Encode space, LF, and CR

```bash
printf 'a b\nc\r\nd' > /tmp/spaces.txt
python3 ascii_unicode_code.py --mode esc-only encode --form esc /tmp/spaces.txt | od -c
```

Expected: `a`, space, `b`, a literal LF, `c`, then
`033 [ U 0 0 0 D m` (CR, encoded), then a literal LF, then `d`.

## 5. Look up a character

The mapping files live in the parent folder:

```bash
grep '^U+00AC,' ../../unicode_mapping.csv
grep '^U+01F600,' ../../unicode_mapping.csv
cat ../../logic_mapping.csv
```

## 6. What is an error here

```bash
python3 ascii_unicode_code.py --mode esc-only encode --form visible /tmp/hello.txt
echo "exit: $?"
python3 ascii_unicode_code.py --mode esc-only convert --to visible /tmp/hello.esc
echo "exit: $?"
```

Both should exit with code 1 and an error naming the mode
restriction. That is by design — this variant has no visible
form.
