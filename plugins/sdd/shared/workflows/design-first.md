# Design-First

Order: design → requirements → tasks. Gate after each (`${CLAUDE_PLUGIN_ROOT}/shared/gate.md`).

## Steps

1. Level. Ask via AskUserQuestion: High-Level (architecture, flows, NFRs) | Low-Level (interfaces, algorithms, pseudocode).
2. Context. Read prompt, constraints, existing architecture files.
   - Done when: every named constraint read.
3. Draft `design.md` at chosen level per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/design.md`. Properties list stays empty until step 5.
   - Done when: artifact's Done-when list holds, minus properties.
4. Gate.
5. Derive `requirements.md` from design per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/requirements.md`. Scope = what design supports.
   - Done when: every component has ≥1 criterion, artifact's Done-when list holds.
6. Gate. Prompt user: "Which user needs does this architecture miss?"
7. Add properties to `design.md` per `${CLAUDE_PLUGIN_ROOT}/shared/correctness.md`. Draft `tasks.md` per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/tasks.md`.
8. Gate. Then tell user: `/spec-run <name>`.

Spec phases write specs only. Code waits for `/spec-run`.
