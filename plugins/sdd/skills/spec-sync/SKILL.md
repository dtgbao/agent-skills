---
name: spec-sync
description: "Sync tasks.md with edited requirements/design and with work already in the codebase."
argument-hint: "<spec-name>"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

Spec: $ARGUMENTS. No name → list `docs/specs/*`, ask which.

Flow: upstream artifact leads, downstream follows.
- Requirements-First, Quick Plan: requirements → design → tasks
- Design-First: design → requirements → tasks
- Bugfix: bugfix → design → tasks

## Steps

1. Load. Read `.spec.json` + three artifacts. List `stale` phases.
2. Upstream first. Stale `design` (feature) or stale `requirements` (design-first) → propose refinement of that artifact, gate (`${CLAUDE_PLUGIN_ROOT}/shared/gate.md`), before tasks.
   - Done when: no stale phase upstream of `tasks`.
3. Coverage. Build matrix: criterion ids ↔ `_Requirements:_` refs ↔ design components.
   - Done when: every criterion, ref, component classified: covered | uncovered | orphan.
4. Evidence. For every unchecked leaf: files named exist? symbols exported? tests exist and pass (run those files only)? Classify `done` (all three) | `partial` | `todo`. Cite path per verdict.
   - Done when: every unchecked leaf classified with evidence.
5. Propose. Table: add leaf (uncovered criterion), edit leaf, remove leaf (orphan), tick leaf (`done`). Show diff. Ask via AskUserQuestion: Apply all | Pick | Cancel.
6. Apply. Keep ticked leaves, user-edited text, `*` marks. Rebuild graph for changed leaves per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/tasks.md`. Set `tasks` phase `approved`.
   - Done when: every criterion covered by ≥1 leaf or user declined; every leaf in exactly one wave.
