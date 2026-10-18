# spec-sync (cart-discount-codes)

## Step 1 — drift
```
DRIFT requirements requirements.md
STALE design
STALE tasks
CHANGED 1.2
AFFECTS 1.2 -> 1.1 1.3
SUSPECT 1.2 -> 3.2 tests/test_api_discounts.py:60 (90)
SUSPECT 1.2 -> 3.2 tests/test_api_discounts.py:120 (90)
RESULT: DRIFT
```
Stale: design, tasks.

## Step 2 — upstream
design.md: no percent bound in text; no change. Gate → Approve.

## Step 3 — coverage
| Item | Class |
|---|---|
| 1.1, 1.3–1.5, 2.1–2.10, 3.1–3.6, 4.1–4.5 | covered |
| 1.2 | changed (1–90 → 1–50); cited by 1.1, 1.3; component Discounts |
| orphans | none |

## Step 4 — evidence
| Leaf | Verdict | Evidence |
|---|---|---|
| 1.1 | todo (AFFECTS) | `shop/discounts.py:69` `not 1 <= value <= 90`; leaf Do text says 1–90 |
| 1.3 | todo (AFFECTS) | `tests/test_discounts.py:38` model `<= 90`; `:102` `st.integers(1, 90)` |
| 3.2 | todo (SUSPECT confirmed) | `tests/test_api_discounts.py:60` and `:120` `st.integers(1, 90)` percent generator = old bound |
| 1.2, 3.1 | done, stays | no 89/90/91 token in `shop/cart.py`, `shop/api.py` |

## Step 5 — proposal
| Action | Target |
|---|---|
| edit leaf | 1.1 Do: "percent value outside 1–90" → "1–50" |
| untick leaf | 1.1, 1.3 (AFFECTS), 3.2 (SUSPECT) |
| untick group | 1, 3 |
| untick checkpoint | 2, 4 |
| add / remove / tick | none |

Answer: Apply all (Script).
