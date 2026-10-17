# Bugfix

Order: bugfix → design → tasks. Gate after each (`${CLAUDE_PLUGIN_ROOT}/shared/gate.md`).

## Steps

1. Facts. Need: exact repro, current result, expected result, behavior that must hold. Any missing → ask via AskUserQuestion (≤4 questions).
   - Done when: all four facts in hand.
2. Draft `bugfix.md` per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/bugfix.md`. Set phase `draft`.
   - Done when: artifact's Done-when list holds.
3. Gate.
4. Investigate. Trace repro through code. Root cause cites `file:line`.
   - Done when: cause explains every Current item.
5. Draft `design.md` (bugfix skeleton) per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/design.md`.
   - Done when: artifact's Done-when list holds.
6. Gate.
7. Draft `tasks.md` in Bugfix order per `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/tasks.md`.
8. Gate. Then tell user: `/spec-run <name>`.

Investigation shows large new functionality → stop, suggest separate feature spec.
