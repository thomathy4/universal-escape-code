# Split mapping file

The full Unicode mapping, `unicode_mapping.csv` (1,114,112 rows + header,
~105 MB), exceeds GitHub's 100 MB per-file limit, so it is stored here as
37 plain-text chunks, each under 3 MB:

- `unicode_mapping.chunk01.csv` … `unicode_mapping.chunk37.csv`

The header row is in `chunk01` only. Concatenating the chunks in order
reproduces the original file exactly. The chunks are each under 3 MB
because the GitHub push path rejects ~9 MB requests with HTTP 413,
while ~3 MB pushes succeed.

## Reassemble

From the repository root, either:

```sh
cat mapping/unicode_mapping.chunk*.csv > unicode_mapping.csv
```

or:

```sh
python3 mapping/reassemble.py
```

`reassemble.py` verifies the result: SHA-256
`2c9163c7c67b8adbab8697c38e580648433d73428c7a23945def5d1826c784ef`
and 1,114,113 lines including the header.

The same file can also be regenerated from scratch with
`python3 generate_mapping.py` (reads `UnicodeData.txt`, Unicode 18.0.0).
