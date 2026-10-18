# Commands (plugin 0.3.4, reused session)

| # | Command | How run | Note |
|---|---|---|---|
| 1 | `/sdd:spec-new Requirements-First: add discount codes to carts. ...` | manual load | Came as a cross-session message in plain text. No skill expansion. Re-read `skills/spec-new/SKILL.md` (0.3.4) from disk. |
| 2 | `/sdd:spec-run discount-codes --mode waves --optional` | manual load | Re-read `skills/spec-run/SKILL.md` (0.3.4). |
| 3 | Hand edit: `requirements.md` percent bound 90 → 50 (lines 5, 18, 37) | human edit (sed) | Text only. No other file touched. |
| 4 | `/sdd:spec-sync discount-codes` | manual load | Re-read `skills/spec-sync/SKILL.md` (0.3.4). |
| 5 | `/sdd:spec-run discount-codes --mode waves --optional` | manual load | Same SKILL.md as #2, re-read. |
