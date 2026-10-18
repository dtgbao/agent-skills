# Bugfix

Order: bugfix → design → tasks. Gate after each (`${CLAUDE_PLUGIN_ROOT}/shared/gate.md`).

## Steps

1. Facts. Need: exact repro, current result, expected result, behavior that must hold. Fact the input implies → state it in the Introduction. Only missing facts → ask via AskUserQuestion (≤4 questions).
   - Done when: all four facts in hand.
2. Investigate. Trace repro through code. Note neighbor paths that share the faulty code. Root cause cites `file:line`.
   - Done when: cause explains every observed symptom.
3. Draft `bugfix.md` per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/bugfix.md`.
   - Done when: artifact's Done-when list holds.
4. Gate.
5. Draft `design.md` per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/bugfix-design.md`.
   - Done when: artifact's Done-when list holds.
6. Gate.
7. Draft `tasks.md` in Bugfix order per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/tasks.md`.
   - Done when: artifact's Done-when list holds.
8. Gate. Then tell user: `/sdd:spec-run <name>`.

Investigation shows large new functionality → stop, suggest a separate feature spec.
