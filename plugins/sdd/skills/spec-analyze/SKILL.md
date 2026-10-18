---
name: spec-analyze
description: "Find gaps, conflicts, and ambiguity in a spec's requirements."
argument-hint: "<spec-name>"
disable-model-invocation: true
allowed-tools: Read, Edit, Glob, Grep, Bash, AskUserQuestion, Agent, Task
---

Spec: $ARGUMENTS. No name → list `docs/specs/*`, ask which. `SPEC` per `${CLAUDE_PLUGIN_ROOT}/shared/state.md`.

## Steps

1. Load. `SPEC drift <dir>`. Read `requirements.md` (or `bugfix.md`) + `.spec.json`. Count criteria = `N0`. Stack + source root from manifest.
   - Done when: file read, state read, `N0` known.
2. Analyze. Dispatch `spec-analyst` subagent (Agent call, `subagent_type: sdd:spec-analyst`, omit `model` (frontmatter `sonnet`), foreground). Give: file path, EARS rules path (`${CLAUDE_PLUGIN_ROOT}/shared/ears.md`, resolved), stack, source root, files the spec names, deferred ids from `## Open Questions`, decided findings (id → chosen option) from earlier rounds, next free finding id, mode `FULL`. Wait for the report; it may arrive as a hand-back message.
   - Done when: findings list or `NO FINDINGS` returned.
3. Resolve. First repair each finding (`CHECK` line missing or not `gaps=1 shall=1 asserts=1` → repair): options that close different gaps → split into separate findings; option with ≠1 `SHALL` → split into criteria; one option that is not `NEEDS_OWNER` → ask A | Defer. Low → defer without asking. High/medium → ask via AskUserQuestion, grouped by affected requirement, ≤4 per call: option A | option B | Defer. `NEEDS_OWNER` → ask the owner question at any severity.
   - Done when: every finding resolved or deferred.
4. Apply. Per criterion, merge every chosen option into one text; show merged text. Option part an existing criterion covers → drop, log it. Option that supersedes a criterion → replace that criterion, log it. New-number clash → renumber, log it. Owner answer that names an interface or type → Glossary or design Data Models note, not a criterion; a behavior → criterion. Then cross-check each changed criterion against every criterion that shares a term with it; clash → treat as a new finding, back to step 3 before the next round. New behavior → new criterion number, never a longer criterion. Check each changed criterion against `${CLAUDE_PLUGIN_ROOT}/shared/ears.md`; split violators. Deferred → `## Open Questions` with id, type, severity.
   Artifact was `approved` → `SPEC edited <dir> requirements`.
   - Done when: every chosen option applied, every changed criterion passes EARS rules.
5. Recheck. Rounds 2–3: dispatch again in mode `FOCUSED`; repeat 3–4. Stop early when a round returns only low or `NO FINDINGS`. After the last apply: dispatch once in mode `VERIFY` with the changed criterion ids. Verify findings: high/medium → one Resolve (step 3) + Apply (step 4), then one more `VERIFY` on only the ids that changed; findings left → `## Open Questions`. Low → `## Open Questions`. Report growth `N0 → N` criteria. Growth >50 % → recommend splitting the spec.
   - Done when: no open high/medium finding outside `## Open Questions`, verify pass done, growth reported.
