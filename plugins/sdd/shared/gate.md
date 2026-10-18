# Gate

Gate = hard stop after one artifact. Next artifact stays undrafted until gate passes. `SPEC` per `${CLAUDE_PLUGIN_ROOT}/shared/state.md`.

1. `SPEC draft <dir> <phase>`. Tasks phase: `SPEC check-tasks <dir>` must print `RESULT: PASS` first. Show path + count line, e.g. `requirements.md: 6 requirements, 20 criteria` · `design.md: 4 components, 6 properties` · `tasks.md: 13 leaves, 6 waves`. Count `### Requirement` headings + numbered criteria; `###` under Components and Interfaces + `### Property`; `N.M` leaves + graph waves. Analyze ran → add criteria growth `N0 → N`.
2. Ask via AskUserQuestion: Approve | Request changes. Requirements phase (any workflow) adds: Analyze first. Recommend it when >8 requirements, money/health/compliance domain, or ambiguity seen.
3. Analyze first → read `${CLAUDE_PLUGIN_ROOT}/skills/spec-analyze/SKILL.md`, run its steps 2–5 for this spec. Back to step 1. Show its open verify findings with the count line.
4. Request changes → ask what. Change may target an earlier artifact: edit it, `SPEC edited <dir> <earlier-phase>` when it was `approved`, gate that artifact first. Then repeat from 1.
5. Approve → `SPEC approve <dir> <phase>`. Joint gate (workflow names two phases) → approve both.

Done when: `.spec.json` phase = `approved`.
