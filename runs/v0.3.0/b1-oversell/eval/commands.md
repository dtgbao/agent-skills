# Commands

| # | Command | Load |
|---|---|---|
| 1 | `/sdd:spec-new Bugfix: two carts can reserve more units than are in stock. ...` | manual load: task text relayed from parent session, no slash expansion in this session; read `plugins/sdd/skills/spec-new/SKILL.md` |
| 2 | `/sdd:spec-run cart-oversell --mode single` | manual load (`plugins/sdd/skills/spec-run/SKILL.md`) |
| 3 | `/sdd:spec-run cart-oversell --mode single --optional` | manual load (`plugins/sdd/skills/spec-run/SKILL.md`) |
