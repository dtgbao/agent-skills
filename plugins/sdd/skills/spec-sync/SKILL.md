---
name: spec-sync
description: "Sync tasks.md with edited requirements/design and with work already in the codebase."
argument-hint: "<spec-name>"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

Spec: $ARGUMENTS. No name → list `docs/specs/*`, ask which. `SPEC` per `${CLAUDE_PLUGIN_ROOT}/shared/state.md`. Upstream artifact leads, downstream follows, in `order`.

## Steps

1. Load. `SPEC drift <dir>`: note `DRIFT` files, `CHANGED` / `ADDED` / `REMOVED` criterion ids, `AFFECTS` and `SUSPECT` leaves. Read `.spec.json` + three artifacts. List `stale` phases.
   - Done when: drift output read, stale list known.
2. Upstream first. Each `stale` phase before `tasks` in `order` → propose refinement so it matches the phases before it, gate (`${CLAUDE_PLUGIN_ROOT}/shared/gate.md`).
   - Done when: no stale phase upstream of `tasks`.
3. Coverage. Matrix: criterion ids ↔ `_Requirements:_` refs ↔ design components. Classify each: covered | uncovered | orphan | changed (text differs from baseline).
   - Done when: every criterion, ref, component classified.
4. Evidence. Every `[x]` leaf in an `AFFECTS` line → `todo` (untick). Every `SUSPECT` hit → read the line; it encodes the old value → `todo`, else note why it stays. Every unchecked leaf: files exist? symbols exported? `Verify` passes? Classify `done` | `partial` | `todo`. Cite path per verdict.
   - Done when: every checked leaf classified with evidence.
5. Propose. Table: add leaf (uncovered), edit leaf (changed), untick leaf (`AFFECTS`, confirmed `SUSPECT`) + its group + every checkpoint after it, remove leaf (orphan), tick leaf (`done`). Show diff. Ask via AskUserQuestion: Apply all | Pick | Cancel.
6. Apply. Keep ticked leaves, user-edited text, `*` marks. Confirmed `SUSPECT` leaf → add the changed criterion id to its `_Requirements:_`, so `spec-run` puts the new text in its runner prompt. Rebuild graph for changed leaves per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/tasks.md`. `SPEC approve <dir> tasks` + every stale phase step 2 did not approve.
   - Done when: `SPEC check-tasks <dir>` prints `RESULT: PASS` or user declined the remaining fails; `.spec.json` has no `stale`.
