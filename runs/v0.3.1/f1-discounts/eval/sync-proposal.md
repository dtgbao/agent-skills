# spec-sync proposal (discount-codes)

## Step 1 — drift
```
DRIFT requirements requirements.md
STALE design
STALE tasks
CHANGED 1.2
AFFECTS 1.2 -> 1.1 1.2
SUSPECT 1.2 -> 3.2 tests/test_cart_discount.py:19 (90)
RESULT: DRIFT
```
Stale: design, tasks.

## Step 2 — upstream
design.md refined (90 → 50, 4 lines), gated, approved.

## Step 3 — coverage
| Criteria | Refs | Component | Class |
|---|---|---|---|
| 1.2 | 1.1, 1.2 | Discounts | changed |
| other 24 | all cited | Discounts / Cart / API | covered |
No uncovered, no orphan.

## Step 4 — evidence
| Leaf | Mark | Verdict | Evidence |
|---|---|---|---|
| 1.1 | [x] | todo | AFFECTS 1.2; `shop/discounts.py:7` `PERCENT_MAX = 90` |
| 1.2 | [x] | todo | AFFECTS 1.2; `tests/test_discounts.py:18,59` hard-code 90 |
| 3.2 | [x] | todo | SUSPECT confirmed: `tests/test_cart_discount.py:19` `st.integers(1, 90)` builds percent codes 51–90, now invalid |
| 3.1 | [x] | stays | no AFFECTS/SUSPECT; `shop/cart.py` has no bound |
| 5.1 | [x] | stays | no AFFECTS/SUSPECT; `shop/api.py` has no bound |
| 5.2 | [x] | stays | no AFFECTS/SUSPECT; `tests/test_api_codes.py` has no 90 |

## Step 5 — proposal
| Action | Target | Change |
|---|---|---|
| edit leaf | 1.1 | Do: `PERCENT_MIN, PERCENT_MAX = 1, 50` |
| edit leaf | 3.2 | Do: add "generate percent `value` from `PERCENT_MIN..PERCENT_MAX` in `shop/discounts.py`" (removes hard-coded bound) |
| untick leaf | 1.1, 1.2, 3.2 | `[x]` → `[ ]` |
| untick group | 1, 3 | `[x]` → `[ ]` |
| untick checkpoint | 2, 4, 6 | every checkpoint after 1.1 |

```diff
-    - Do: ... `PERCENT_MIN, PERCENT_MAX = 1, 90`.
+    - Do: ... `PERCENT_MIN, PERCENT_MAX = 1, 50`.
```
```diff
     - Do: Add examples: second `apply_code` raises ...
+    - Do: Generate percent `value` from `PERCENT_MIN..PERCENT_MAX` imported from `shop/discounts.py`; no hard-coded bound.
```
Options: Apply all | Pick | Cancel
