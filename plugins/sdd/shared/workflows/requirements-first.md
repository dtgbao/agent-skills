# Requirements-First

Order: requirements → design → tasks. Gate after each (`${CLAUDE_PLUGIN_ROOT}/shared/gate.md`). Spec phases write specs only. Code waits for `/sdd:spec-run`.

## Steps

1. Context. Read user prompt, files it names, pasted docs. Stack + test/typecheck commands from manifest or README.
   - Done when: every named file read, stack known.
2. Draft `requirements.md` per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/requirements.md`.
   - Done when: artifact's Done-when list holds.
3. Gate.
4. Draft `design.md` per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/design.md`. Properties per `${CLAUDE_PLUGIN_ROOT}/shared/correctness.md` steps 1–3.
   - Done when: artifact's Done-when list holds.
5. Gate.
6. Draft `tasks.md` per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/tasks.md`.
   - Done when: artifact's Done-when list holds.
7. Gate. Then tell user: `/sdd:spec-run <name>`.
