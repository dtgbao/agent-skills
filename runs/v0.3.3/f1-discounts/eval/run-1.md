# spec-run report, run 1 (`--mode waves --optional`)

| Leaf | Size | Model | Attempts | Status | Tests | Counterexample |
|---|---|---|---|---|---|---|
| 1.1 | M | sonnet | 1 | done | Verify one-liner ok | none |
| 1.2* | M | sonnet | 1 | done | test_discounts.py 7 passed | none |
| 3.1 | M | sonnet | 1 | done | test_cart.py 3 passed + one-liner | none |
| 3.2* | M | sonnet | 1 | done | test_cart_discount.py 3 passed | none |
| 5.1 | M | sonnet | 1 | done | full suite 10 passed | none |
| 5.2* | S | haiku | 1 | done | test_api_discount.py 9 passed | none |

Checkpoints: 2 → 10 passed, 4 → 13 passed, 6 → 22 passed. All `[x]`. No `[-]` left.
