# Commands

| # | Command | Invocation | Notes |
|---|---|---|---|
| 1 | `/sdd:spec-new Requirements-First: add discount codes to carts. ...` | manual load | Arrived as task text from parent session, no slash expansion. Read `/Users/baodang/Documents/code/agent-skills/plugins/sdd/skills/spec-new/SKILL.md`. |
| 2 | `/sdd:spec-run discount-codes --mode waves --optional` | manual load | Read `skills/spec-run/SKILL.md`; `$ARGUMENTS` = `discount-codes --mode waves --optional`. |
| 3 | Hand edit: `requirements.md` 1.2 `1–90` → `1–50` | human edit (sed) | Text only; no other file touched. |
| 4 | `/sdd:spec-sync discount-codes` | manual load | Read `skills/spec-sync/SKILL.md`. |
| 5 | `/sdd:spec-run discount-codes --mode waves --optional` | manual load | Second run, scope from sync unticks. |
