# spec-run reserve-oversell --mode single --optional (cmd 3)

Drift: NO DRIFT. check-tasks: PASS. Scope: 4.1* only. Pin 1.1 is `[x]` with fix 2.1 `[x]`, so not in scope.

| Leaf | Size | Model | Attempts | Status | Tests | Counterexample |
|---|---|---|---|---|---|---|
| 4.1* | S | haiku | 1 | done | 1 pass | none |
| 5 Checkpoint (re-run: leaf above ran) | – | – | – | green `[x]` | 14 passed | – |

Checkpoint 3 not re-run: no leaf above it ran this run. No `[-]` left.
