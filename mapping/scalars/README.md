# Split scalars mapping file

The scalars mapping, `unicode_mapping_scalars.csv` (1,112,064 rows +
header, ~110 MB), exceeds GitHub's 100 MB per-file limit, so it is
stored here as 37 plain-text chunks, each under 3 MB:

- `unicode_mapping_scalars.chunk01.csv` … `unicode_mapping_scalars.chunk37.csv`

The header row is in `chunk01` only. Concatenating the chunks in order
reproduces the original file exactly. The chunks are each under 3 MB
because the GitHub push path rejects ~9 MB requests with HTTP 413,
while ~3 MB pushes succeed.

This file holds one row per scalar value (U+0000–U+10FFFF except the
2,048 surrogates). It is the same mapping as `unicode_mapping.csv`
with the surrogate rows removed. Columns are the same:
codepoint, definition, decimal, status, esc_form, visible_form,
logic_alias.

## Reassemble

From the repository root, either:

```sh
cat mapping/scalars/unicode_mapping_scalars.chunk*.csv > unicode_mapping_scalars.csv
```

or:

```sh
python3 mapping/scalars/reassemble.py
```

`reassemble.py` verifies the result: SHA-256
`80f890328a797eecca4f5aa451d793358c21a48ee8eba47eca982d022be08a07`
and 1,112,065 lines including the header.
