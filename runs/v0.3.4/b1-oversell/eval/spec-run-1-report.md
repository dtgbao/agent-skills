# spec-run report (cmd 2: --mode single)

| Leaf | Size | Model | Attempts | Status | Tests | Counterexample |
|---|---|---|---|---|---|---|
| 1.1 | S | haiku | 1 | done (red, expected) | repro 0/3 before fix | s=1, h=1, q=1 (expected red; step 6 exempt) |
| 1.2 | M | sonnet | 1 | done | keep_inventory 4/4 | none |
| 1.3 | S | haiku | 1 | done | keep_cart 3/3 | none |
| 2.1 | S | haiku | 1 | done | 13/13 | none |
| 4.1* | M | — | 0 | optional skipped | — | — |

Checkpoint 3: 13 passed. Checkpoint 5: 13 passed (4.1 out of scope). Group 4 stays `[ ]`.
