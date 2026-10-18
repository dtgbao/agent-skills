# Design-First

Order: design → requirements → tasks. Gate after design, joint gates after. `SPEC` per `${CLAUDE_PLUGIN_ROOT}/shared/state.md`. Spec phases write specs only. Code waits for `/sdd:spec-run`.

## Steps

1. Level. Ask via AskUserQuestion: High-Level (architecture, flows, NFRs) | Low-Level (interfaces, algorithms, pseudocode).
2. Context. Read prompt, constraints, existing architecture files. Stack + test/typecheck commands from manifest or README.
   - Done when: every named constraint read.
3. Draft `design.md` at chosen level per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/design.md`. Leave `_Requirements:_`, Criteria Classification, Correctness Properties empty.
   - Done when: artifact's Done-when list holds, minus those three.
4. Gate (`${CLAUDE_PLUGIN_ROOT}/shared/gate.md`).
5. Derive `requirements.md` per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/requirements.md`. Scope = what design supports. Add `_Requirements:_` lines to design components.
   - Done when: every component cites ≥1 criterion, every criterion cited by ≥1 component, artifact's Done-when list holds.
6. Joint gate: requirements + design. Ask with the gate: "Which user needs does this architecture miss?"
   - Answer names needs the design supports → add requirements, repeat 6.
   - Need the design cannot support → Request changes on design (`${CLAUDE_PLUGIN_ROOT}/shared/gate.md` step 4), redo 5.
   - Approve → `SPEC approve <dir> design requirements`.
7. Add Criteria Classification + Correctness Properties to `design.md` per `${CLAUDE_PLUGIN_ROOT}/shared/correctness.md` steps 1–3. Draft `tasks.md` per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/tasks.md`.
   - Done when: both Done-when lists hold.
8. Joint gate: tasks + design properties. Approve → `SPEC approve <dir> design tasks`. Then tell user: `/sdd:spec-run <name>`.
