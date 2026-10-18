# Commands

| # | Command | Invocation | Notes |
|---|---|---|---|
| 1 | `/sdd:spec-new Requirements-First: add discount codes to carts. ...` | manual load | Task came as text from parent session, not as an expanded slash command. Read `skills/spec-new/SKILL.md`. |
| 2 | `/sdd:spec-run cart-discount-codes --mode waves --optional` | manual load | Read `skills/spec-run/SKILL.md`. |
| 3 | Hand edit: `requirements.md` percent bound 90 → 50 | human edit (sed) | Two lines changed: Glossary Discount_Value and criterion 1.2. No other file touched. No SPEC call. |
| 4 | `/sdd:spec-sync cart-discount-codes` | manual load | Read `skills/spec-sync/SKILL.md`. |
| 5 | `/sdd:spec-run cart-discount-codes --mode waves --optional` | manual load | Scope: 1.1, 1.3*, 3.2* (unticked by sync). |
