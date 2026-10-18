# spec-run report (cmd 2: --mode single)

| Leaf | Size | Model | Attempts | Status | Tests | Counterexample |
|---|---|---|---|---|---|---|
| 1.1 | S | haiku | 1 | done (red as expected) | test_oversell_pin.py 0/3 pass before fix | none (expected red) |
| 1.2 | M | sonnet | 1 | done | test_oversell_preservation.py 5/5 | none |
| 2.1 | S | haiku | 1 | done | pins + test_cart 11/11 | none |
| 4.1* | S | — | 0 | optional skipped | — | — |

Checkpoint 3: 11 passed. Checkpoint 5: 11 passed. Group 4 stays `[ ]` (optional skipped).
