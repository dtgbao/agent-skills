# sdd

Spec-driven development for Claude Code.

```
requirements.md | bugfix.md  →  design.md  →  tasks.md  →  run
```

Specs live in `docs/specs/<name>/`. Commit them with code.

## Commands

| Command | Does |
|---|---|
| `/sdd:spec-new [idea]` | Pick workflow (Requirements-First, Design-First, Bugfix, Quick Plan), draft artifacts, gate each |
| `/sdd:spec-analyze <name>` | Cross-requirement review: conflicts, ambiguity, missing edge/failure cases |
| `/sdd:spec-sync <name>` | Align `tasks.md` with edited upstream artifacts + code already written |
| `/sdd:spec-run <name> [task-id] [--mode single\|waves] [--optional]` | Run tasks: one at a time, or parallel waves via subagents |

## Layout

```
.claude-plugin/plugin.json
skills/spec-{new,analyze,sync,run}/SKILL.md   user-invoked, zero context load
agents/spec-task-runner.md                    one task per dispatch
agents/spec-analyst.md                        read-only requirements review
shared/                                       plain files, any skill points at them
  state.md  gate.md  ears.md  correctness.md
  workflows/  artifacts/
```

## Design notes

- All four skills set `disable-model-invocation: true`: you type them, no description sits in context.
- Shared reference lives outside the skill system, so skills reach it without descriptions.
- Each workflow file loads only on its branch.
- Every step ends on a checkable Done-when line.
- Subagents see one task or one document. Later steps stay out of their view.

## Test locally

```bash
claude --plugin-dir ./sdd
```

Check that `${CLAUDE_PLUGIN_ROOT}` paths in skill text resolve. Path fails → swap for paths relative to each `SKILL.md`.
