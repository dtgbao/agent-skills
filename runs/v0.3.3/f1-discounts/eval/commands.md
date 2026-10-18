# Commands

| # | Command | How run | Note |
|---|---|---|---|
| 1 | `/sdd:spec-new Requirements-First: add discount codes to carts. ...` | manual load | First message came from another session as plain text. No skill expansion seen. Read `skills/spec-new/SKILL.md`. |
| 2 | `/sdd:spec-run cart-discount-codes --mode waves --optional` | manual load | Read `skills/spec-run/SKILL.md`. Skills are user-invoked; I cannot invoke them. |
| 3 | Hand edit: requirements.md percent bound 90 → 50 (lines 5, 14, 35) | human edit (sed) | Text only. No other file touched. |
| 4 | `/sdd:spec-sync cart-discount-codes` | manual load | Read `skills/spec-sync/SKILL.md`. |
| 5 | `/sdd:spec-run cart-discount-codes --mode waves --optional` | manual load | Same SKILL.md as #2. |
