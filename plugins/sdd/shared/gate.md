# Gate

Gate = hard stop after one artifact. Next artifact stays undrafted until gate passes. `SPEC` per `${CLAUDE_PLUGIN_ROOT}/shared/state.md`.

1. `SPEC draft <dir> <phase>`. Tasks phase: `SPEC check-tasks <dir>` must print `RESULT: PASS` first. Show path + count line, e.g. `requirements.md: 6 requirements, 20 criteria` · `bugfix.md: 2 current, 2 expected, 3 unchanged` · `design.md: 4 components, 6 properties` · `tasks.md: 13 leaves, 6 waves, seams: <list>`. Count `### Requirement` headings + numbered criteria; `###` under Components and Interfaces + `### Property`; `N.M` leaves + graph waves + distinct `Seam` values (the user confirms the seams at this gate). Analyze ran → add criteria growth `N0 → N`.
2. Ask via AskUserQuestion: Approve | Request changes. Requirements phase (any workflow) adds: Analyze first. Recommend it when >30 criteria (bugfix: >12 items), money/health/compliance domain, or ambiguity seen.
3. Analyze first → read `${CLAUDE_PLUGIN_ROOT}/skills/spec-analyze/SKILL.md`, run its steps 2–6 for this spec. Back to step 1. Show the items kept deferred with the count line.
4. Request changes → ask what. Change may target an earlier artifact: edit it, `SPEC edited <dir> <earlier-phase>` when it was `approved`, gate that artifact first. Then repeat from 1.
5. Approve → `SPEC approve <dir> <phase>`. Joint gate (workflow names two phases) → approve both.

Done when: `.spec.json` phase = `approved`.
