# spec-run report, run 2 (`--mode waves --optional`)

Scope: 1.1, 1.2*, 3.2* (unticked by spec-sync). 3.1, 5.1, 5.2* stay `[x]`.

| Leaf | Size | Model | Attempts | Status | Tests | Counterexample |
|---|---|---|---|---|---|---|
| 1.1 | M | sonnet | 1 | done | Verify ok; `PERCENT_RANGE = (1, 50)` | none |
| 1.2* | M | sonnet | 1 | done | test_discounts.py 3 passed | none |
| 3.2* | M | sonnet | 1 | done | test_cart_codes.py 3 passed | none |

Checkpoint 2 after wave 1: red on `tests/test_cart_codes.py` (3.2's file) → deferred. After 3.2: checkpoints 2, 4, 6 → 16 passed.
