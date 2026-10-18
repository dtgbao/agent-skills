# Commands (plugin 0.3.4, reused session)

| # | Command | Load |
|---|---|---|
| 1 | `/sdd:spec-new Bugfix: two carts can reserve more units than are in stock. With stock 5 for MUG-01, cart A adds 3 and cart B adds 3; both succeed and available becomes -1.` | manual load: command came as a cross-session message, no slash expansion. Read `/Users/baodang/Documents/code/agent-skills/plugins/sdd/skills/spec-new/SKILL.md` (0.3.4, re-read from disk) |
| 2 | `/sdd:spec-run stock-overbooking --mode single` | manual load. Read `/Users/baodang/Documents/code/agent-skills/plugins/sdd/skills/spec-run/SKILL.md` (0.3.4) |
| 3 | `/sdd:spec-run stock-overbooking --mode single --optional` | manual load (spec-run SKILL.md re-read from disk) |
