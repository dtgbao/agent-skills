# sdd

Spec-driven development for Claude Code, Kiro-style.

```
(brainstorm)  →  requirements.md | bugfix.md  →  design.md  →  tasks.md  →  run
```

Brainstorm sits outside the workflow. It writes no files: it ends on a playback the user confirms in chat.

Specs live in `docs/specs/<name>/`. Commit them with code.

## Install

```text
/plugin marketplace add dtgbao/agent-skills
/plugin install sdd@bao-plugins
```

## Commands

| Command | Does |
|---|---|
| `/sdd:spec-brainstorm [idea]` | Clarify a vague feature idea: open questions, then grill rounds with recommendations, then a playback the user confirms. Writes no files. `spec-new` runs it on vague or ambiguous input |
| `/sdd:spec-new [idea \| name]` | Pick workflow (Requirements-First, Design-First, Bugfix, Quick Plan), draft artifacts, gate each. Existing name → resume. Empty input → uses the confirmed brainstorm playback |
| `/sdd:spec-analyze <name>` | Cross-requirement review: conflicts, ambiguity, missing edge/failure cases. Round 1 full, rounds 2–3 focused on conflicts, then a verify pass. Reports criteria growth |
| `/sdd:spec-sync <name>` | Detect hand edits, realign `tasks.md` with upstream artifacts and code already written |
| `/sdd:spec-run <name> [task-id] [--mode single\|waves] [--optional]` | Run leaves: one at a time, or parallel waves via subagents |

## State

`.spec.json` holds phase states (`pending → draft → approved`, `stale`), a sha256 per approved artifact, and criterion text taken at tasks approval. `shared/scripts/spec.py` writes all state and checks `tasks.md`:

```bash
python3 shared/scripts/spec.py drift docs/specs/<name>        # hand edits → DRIFT, criterion changes → CHANGED
python3 shared/scripts/spec.py check-tasks docs/specs/<name>  # graph, deps, disjoint files, coverage
```

A hand edit of an approved file marks later phases `stale` at the next skill load. `/sdd:spec-sync` then unticks leaves that cite changed criteria, and leaves whose files still hold the old value (`SUSPECT`).

## Layout

```
.claude-plugin/plugin.json
plugin.json                                   Agent Plugins manifest
skills/spec-{brainstorm,new,analyze,sync,run}/SKILL.md   user-invoked, zero context load
agents/spec-task-runner.md                    one leaf per dispatch
agents/spec-analyst.md                        read-only requirements review
shared/                                       plain files, any skill points at them
  state.md  gate.md  ears.md  correctness.md  visuals.md
  workflows/  artifacts/  scripts/spec.py
```

## Design notes

- All five skills set `disable-model-invocation: true`: you type them, no description sits in context.
- Shared reference lives outside the skill system, so skills reach it without descriptions.
- Each workflow file loads only on its branch.
- Brainstorm vs analyze: brainstorm fixes intent (who, why, scope) before any criterion exists. `spec-analyze` finds gaps in written criteria.
- Every step ends on a checkable Done-when line. Deterministic checks (state, graph) run in `spec.py`, not in the model.
- Subagents see one leaf or one document. Later steps stay out of their view.
- Task leaves carry `Files`, `Kind`, `Size`, `Do`, `Verify`, `_Requirements:_`, so a runner acts without reading the whole design.
- Cost routing: leaf `Size` S/M/L → runner model haiku/sonnet/opus. A retry moves one tier up. Agents default to `sonnet`. Hosts that ignore `model` run the session model.

## Evals

Eval harness, mock projects and open issues live outside the plugin, in [`evals/sdd/`](../../evals/sdd/README.md), so installs stay small. Raw run output is on branch `eval-runs`.

## Test locally

From the repo root:

```bash
claude --plugin-dir plugins/sdd
```

Check that `${CLAUDE_PLUGIN_ROOT}` paths in skill text resolve. Path fails → swap for paths relative to each `SKILL.md`.
