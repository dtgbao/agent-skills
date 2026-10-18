# Spec state

Dir `docs/specs/<name>/`. State `docs/specs/<name>/.spec.json`. `SPEC <cmd> <args>` = run `python3 ${CLAUDE_PLUGIN_ROOT}/shared/scripts/spec.py <cmd> <args>` as one full command line (a shell variable does not word-split in zsh). Every state write goes through `SPEC`. No `python3` → edit `.spec.json` by hand per Events table.

```json
{
  "name": "<name>",
  "workflow": "requirements-first | design-first | bugfix | quick-plan",
  "order": ["requirements", "design", "tasks"],
  "phases": { "requirements": "pending", "design": "pending", "tasks": "pending" },
  "hashes": { "requirements": "", "design": "", "tasks": "" },
  "criteria": {}
}
```

- `order`: design-first → `design, requirements, tasks`. Others → `requirements, design, tasks`.
- Phase file: requirements → `requirements.md` (`bugfix.md` when workflow = bugfix). design → `design.md`. tasks → `tasks.md`.
- `hashes`: sha256 of phase file at approval. `criteria`: criterion text at tasks approval = baseline that tasks were built on.
- `workflow` fixed for spec life. Change needed → new spec, copy content.

## Events

| Event | Command | Effect |
|---|---|---|
| Spec created | `SPEC init <dir> <workflow>` | all phases `pending` |
| Artifact shown at gate | `SPEC draft <dir> <phase>` | phase → `draft` |
| Gate Approve, sync Apply | `SPEC approve <dir> <phase>...` | phase → `approved`, `stale` cleared, hash stored. `tasks`: refused while `check-tasks` fails; stores criteria baseline |
| Skill edits approved file with user consent | `SPEC edited <dir> <phase>` | hash stored. Later non-`pending` phases in `order` → `stale` |
| Load in any skill | `SPEC drift <dir>` | Hand edit of approved file → `DRIFT <phase>`, later phases → `stale`. Criterion text vs baseline → `CHANGED` / `ADDED` / `REMOVED <id>`, then `AFFECTS <id> -> <leaf ids>` (leaves citing it) and `SUSPECT <id> -> <leaf> <file:line>` (other leaves whose files still hold a number gone from the criterion). Checkbox marks in `tasks.md` never count as drift |

## Route by phase

Skill needs a phase `approved` and finds:

| Phase | Next command |
|---|---|
| `pending` or `draft` | `/sdd:spec-new <name>` (resume) |
| `stale` | `/sdd:spec-sync <name>` |
