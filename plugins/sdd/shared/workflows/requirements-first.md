# Requirements-First

Order: requirements → design → tasks. Gate after each (`${CLAUDE_PLUGIN_ROOT}/shared/gate.md`).

## Steps

1. Context. Read user prompt, files it names, pasted docs. Stack from manifest.
   - Done when: every named file read.
2. Draft `requirements.md` per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/requirements.md`. Set phase `draft`.
   - Done when: artifact's Done-when list holds.
3. Gate. Offer `/spec-analyze` first when: >8 requirements, money/health/compliance domain, or ambiguity seen.
4. Draft `design.md` per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/design.md`. Properties per `${CLAUDE_PLUGIN_ROOT}/shared/correctness.md`.
   - Done when: artifact's Done-when list holds.
5. Gate.
6. Draft `tasks.md` per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/tasks.md`.
   - Done when: artifact's Done-when list holds.
7. Gate. Then tell user: `/spec-run <name>`.

Spec phases write specs only. Code waits for `/spec-run`.
