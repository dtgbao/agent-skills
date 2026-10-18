---
name: spec-run
description: "Run tasks from a spec's tasks.md, one at a time or in parallel waves."
argument-hint: "<spec-name> [task-id] [--mode single|waves] [--optional]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Agent, Task
---

Arguments: $ARGUMENTS. `SPEC` per `${CLAUDE_PLUGIN_ROOT}/shared/state.md`. Orchestrator (you) owns `tasks.md` and `.spec.json`. `spec-task-runner` subagents own code.

## Steps

1. Load. `SPEC drift <dir>`. Read `.spec.json`. Any phase not `approved` → stop, give next command per Route table in `${CLAUDE_PLUGIN_ROOT}/shared/state.md`.
2. Mode. `--mode` given → use it. `task-id` given → `single`. Else ask via AskUserQuestion: single (approve each) | waves (all, parallel).
3. Scope. `task-id` given → that leaf only. Else leaves `[ ]` or `[-]` (left by a stopped run). Drop `*` leaves unless `--optional`. `Expect: red` pin with a `[x]` fix leaf (`Kind: code` leaf whose `deps` hold the pin) → drop, report "pin after fix". Scope empty → report "nothing to run" + reason, stop.
4. Graph. `SPEC check-tasks <dir>`. `RESULT: FAIL` → show fails, stop, point to `/sdd:spec-sync <name>`.
5. Execute, wave by wave in id order. Wave ∩ scope = leaves.
   - **single**: per leaf, show it, ask Run | Skip | Stop. Run → mark `[-]`, dispatch one `spec-task-runner`.
   - **waves**: mark each `[-]`. Dispatch one `spec-task-runner` per leaf, all in ONE message.
   - Dispatch = Agent call, `subagent_type: sdd:spec-task-runner`, foreground. Tiers: haiku → sonnet → opus. `model` from leaf `Size`: S → `haiku`, M → `sonnet`, L → `opus`. No `Size` → omit `model` (agent default `sonnet`). Prompt: spec dir, leaf id, full leaf text, the text of every criterion in its `_Requirements:_`, correctness rules path (`${CLAUDE_PLUGIN_ROOT}/shared/correctness.md`, resolved). Wait for every report before marking. A report may arrive as a hand-back message, not in the Agent result: read it there.
   - After reports: `done` → `[x]`. `FOREIGN-FAIL` files → note them for the checkpoint. `failed` with a COUNTEREXAMPLE → `[ ]`, go to step 6. Other `failed`/`blocked`, or no `STATUS:` line → `[ ]`, show the raw reply, ask Retry | Skip (dependents skip too) | Stop. Retry moves the leaf one tier up; opus stays opus.
   - Group → `[x]` when every leaf in it is `[x]`. Skipped `*` leaves keep it `[ ]`; report "optional skipped".
   - Checkpoint, once every in-scope leaf above it is `[x]`: run its commands. Failing test file in `Files` of an in-scope leaf not yet run → defer the checkpoint until that leaf runs. Re-run an `[x]` checkpoint when a leaf above it ran this run. Only open leaves above it are skipped `*` leaves → run it too. Green → `[x]`. Red → show output, name the leaf whose `Files` hold the failing test, ask Untick leaf | Continue | Stop.
6. Property failure. Report holds counterexample, and the leaf is not an `Expect: red` pin with STATUS `done` → ask per step 5 of `${CLAUDE_PLUGIN_ROOT}/shared/correctness.md`:
   - fix implementation → re-dispatch each code leaf in the test leaf's `deps` with the counterexample, same tier; then re-run the test leaf.
   - fix test → re-dispatch the test leaf with the counterexample and the user's note, same tier.
   - fix requirement → stop; user edits the criterion, then `/sdd:spec-sync <name>`.
7. Report. Table: leaf, size, model, attempts, status, tests, counterexample.
   - Done when: every in-scope leaf is `[x]` or listed with reason; no `[-]` left.
