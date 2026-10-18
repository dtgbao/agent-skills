# Commands

| # | Command | Invocation | Notes |
|---|---|---|---|
| 1 | `/sdd:spec-analyze gift-cards` | manual load | Task text came from the parent session as a plain message, not a slash expansion. Read `/Users/baodang/Documents/code/agent-skills/plugins/sdd/skills/spec-analyze/SKILL.md`, `${CLAUDE_PLUGIN_ROOT}` = `/Users/baodang/Documents/code/agent-skills/plugins/sdd`, `$ARGUMENTS` = `gift-cards`. |
| 2 | `/sdd:spec-new gift-cards` (resume) | manual load | Requested by parent session as plain text. Read `.../skills/spec-new/SKILL.md`, then `shared/workflows/requirements-first.md`, `shared/gate.md`, `shared/artifacts/{design,tasks}.md`, `shared/correctness.md`, `shared/visuals.md`. `$ARGUMENTS` = `gift-cards`. |
| 3 | `/sdd:spec-run gift-cards --mode waves --optional` | manual load | Requested by parent session as plain text. Read `.../skills/spec-run/SKILL.md` and `agents/spec-task-runner.md`. `$ARGUMENTS` = `gift-cards --mode waves --optional`. |
