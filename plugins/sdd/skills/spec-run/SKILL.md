---
name: spec-run
description: "Run tasks from a spec's tasks.md, one at a time or in parallel waves."
argument-hint: "<spec-name> [task-id] [--mode single|waves] [--optional]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Task
---

Arguments: $ARGUMENTS

Orchestrator (you) owns `tasks.md` and `.spec.json`. `spec-task-runner` subagents own code.

## Steps

1. Load. Read `.spec.json`. `tasks` phase not `approved` → stop, point to `/spec-sync`.
2. Mode. `--mode` given → use it. `task-id` given → `single`. Else ask via AskUserQuestion: single (approve each) | waves (all, parallel).
3. Scope. Leaves marked `[ ]`. Drop `*` leaves unless `--optional`. Done leaves stay out.
4. Graph. Check wave rules in `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/tasks.md`. Broken → stop, point to `/spec-sync`.
5. Execute.

   **single**, per leaf in wave order:
   1. Show leaf. Ask: Run | Skip | Stop.
   2. Mark `[-]`. Dispatch one `spec-task-runner`.
   3. `done` → mark `[x]`. Else show report.

   **waves**, per wave in id order:
   1. Wave ∩ scope = leaves. Mark each `[-]`.
   2. Dispatch one `spec-task-runner` per leaf, all in ONE message (parallel Task calls).
   3. Collect reports. `done` → `[x]`. `failed`/`blocked` → back to `[ ]`.
   4. Failures → ask: Retry failed | Skip failed (dependents skip too) | Stop.
   5. Checkpoint whose earlier groups all complete → run test + typecheck scripts from manifest. Red → show output, ask user.

6. Property failure. Report holds counterexample → follow step 5 of `${CLAUDE_PLUGIN_ROOT}/shared/correctness.md`.
7. Report. Table: leaf, status, tests, counterexample.
   - Done when: every in-scope leaf is `[x]` or listed with reason.
