# spec-run reserve-oversell --mode single (cmd 2)

Drift: NO DRIFT. check-tasks: PASS. Scope: 1.1, 1.2, 2.1 (4.1 `*` dropped, no `--optional`).

| Leaf | Size | Model | Attempts | Status | Tests | Counterexample |
|---|---|---|---|---|---|---|
| 1.1 | M | sonnet | 1 | done (red as expected) | 0 pass / 3 fail | stock=1, ops=[(0,1),(0,1)] |
| 1.2 | M | sonnet | 1 | done (green) | 7 pass | none |
| 2.1 | S | haiku | 1 | done | 13 pass | none |
| 3 Checkpoint | – | – | – | green `[x]` | 13 passed | – |
| 4.1* | S | – | – | optional skipped | – | – |
| 5 Checkpoint | – | – | – | green `[x]` (all in-scope leaves above it `[x]`) | 13 passed | – |

Group 4 stays `[ ]`: optional skipped.
