# ascii-unicode-logic — portable skill folder

General skill/prompt for the ASCII/ANSI code for sentential logic and
Unicode (Unicode 18.0.0, code v1.1.0).

## Contents

| File | Definition |
|---|---|
| `SKILL.md` | The skill: when to use it, the two forms, how to run the script, text-only fallback, and the compact paste prompt. |
| `skill.yaml` | Muse-only companion file; harmless in other apps. |
| `scripts/ascii_unicode_code.py` | Encoder/decoder, Python 3.10+ stdlib only. CLI: `encode` / `decode` / `convert`, `--mode both\|esc-only\|visible-only`. |
| `references/SPEC.md` | Full spec, v1.1.0. |
| `references/HOWTO.md` | Step-by-step tasks. |
| `references/SYMBOLS.md` | Every logic symbol defined, symbol first, definition second. |
| `references/logic_mapping.csv` | Logic inventory only, 18 rows. |

## Install

- **Native Agent Skills apps** (Claude Code, Codex, Gemini CLI, Cursor,
  GitHub Copilot, Mistral Vibe Code, Grok Build, Muse Code, Manus,
  OpenClaw): copy this folder to `.agents/skills/ascii-unicode-logic/`
  (plus `.claude/skills/` for Claude Code where needed).
- **Chat apps with Skills upload** (Claude, ChatGPT, Gemini): zip this
  folder and upload it as a skill. Do NOT add `unicode_mapping.csv`.
- **Paste-only apps** (DeepSeek, Meta AI, Grok chat, Perplexity, Copilot
  chat, Lovable, Base44, PocketPal, Joey): paste the compact prompt at
  the end of `SKILL.md` into Custom Instructions / Project / Space /
  Pal instructions, every new chat/project as the app requires.
- **Muse**: paste the compact prompt + attach the script, SPEC, and
  logic CSV, and ask Muse to save it under
  `~/workspace/custom-skills/ascii-unicode-logic/`, then run the test
  below and verify in a new chat.

## Test

```sh
printf '¬(p ∧ q) → r\n' | python3 scripts/ascii_unicode_code.py --mode both encode --form visible
```

Expected visible form: `\u00AC(p \u2227 q) \u2192 r`.

## Do not upload the full mapping

`unicode_mapping.csv` (1,114,112 rows, 105 MB) is deliberately NOT in
this folder. It exceeds chat-app size and file-count limits. Keep it
beside the skill for tier-1 coding agents / Muse's VM only. The full
CSV can be regenerated with `generate_mapping.py` + `UnicodeData.txt`
from the parent project, or reassembled from the split chunks in
`mapping/` (see the parent README).
