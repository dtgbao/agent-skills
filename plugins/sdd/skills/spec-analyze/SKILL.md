---
name: spec-analyze
description: "Find gaps, conflicts, and ambiguity in a spec's requirements before design."
argument-hint: "<spec-name>"
disable-model-invocation: true
allowed-tools: Read, Edit, Glob, Grep, AskUserQuestion, Task
---

Spec: $ARGUMENTS. No name → list `docs/specs/*`, ask which.

## Steps

1. Load. Read `requirements.md` (or `bugfix.md`) + `.spec.json`.
   - Done when: file read, state read.
2. Analyze. Dispatch `spec-analyst` subagent with file path. Subagent returns findings.
   - Done when: findings list or `NO FINDINGS` returned.
3. Resolve. Walk findings high → low. Ask via AskUserQuestion (group related, ≤4 per call): option A | option B | Defer.
   - Done when: every finding resolved or deferred.
4. Apply. Edit artifact per chosen options. Deferred → append under `## Open Questions`.
   Artifact was `approved` → mark later phases `stale` per `${CLAUDE_PLUGIN_ROOT}/shared/state.md`.
5. Recheck. Dispatch `spec-analyst` again. Repeat steps 3–4 until `NO FINDINGS` or only deferred remain. Max 3 rounds.
   - Done when: no open non-deferred finding.
