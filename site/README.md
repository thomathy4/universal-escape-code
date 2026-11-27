# The symbology site

A static site built from this project's own symbol data: plain HTML, SVG and
JavaScript, no backend. Every unit is one cell — its encoded character under
its name on the left, its definition on the right.

- `index.html` — master page: every set, every combination set, the learner
- `units/set-*.html` — one page per subset of units
- `combos/comb-*.html` — combinations, with definitions composed by rule
- `learner.html` — deconstruct a definition to its units, rebuild it, train
- `data/corpus.js` — the units, rules and combinations, as plain JavaScript
- `assets/` — shared CSS and JavaScript

Regenerate after changing `logic_mapping.csv`, the mapping CSVs, or the
generator:

```
python3 site/build_site.py
```

The generator is stdlib-only Python 3 and deterministic: it rewrites every
page in place. Serve the directory with any file server
(`python3 -m http.server 3000 --directory site`).

State lives in cookies: visited units, the row you were on, the tour position,
and the learner's weights. Nothing is sent anywhere.
