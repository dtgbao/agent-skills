# QA log

## Q1 — Requirements gate (round 0)
Shown: `requirements.md: 4 requirements, 22 criteria`
Question: Approve | Request changes | Analyze first (Recommended: money domain)
Answer (Script): Analyze first

## Q2 — Analyze round 1, Requirement 2 (F1, F2)
- F1 (medium): A) 2.8 fixed check order, `already applied` before expiry | B) order with `already applied` last | Defer → **A** (Script)
- F2 (medium): A) 2.8 missing/bad `ctx["today"]` → ValueError | B) 500 `bad clock` | Defer → **A** (Script)

## Q3 — Analyze round 1, Requirement 4 (F3)
- F3 (medium): A) 4.5 bad line body (`unit_price_cents`, `quantity`) → 400 `bad line` | B) NEEDS_OWNER line fields | Defer → **A** (Script)
- Note: option A names fields `unit_price_cents`/`quantity`. The real API takes `sku`/`qty` and reads price from `CATALOG`. The analyst sees only requirements.md. Applied verbatim per Script; logged as an issue.

F4 (low): deferred without asking (skill step 3).

## Q4 — Analyze round 2, Requirement 2 (F6, F7, F8)
- F6 (medium): A) 2.1 success = no error in 2.2–2.7 | Defer → **A** (Script)
- F7 (medium): A) 2.10 accept `a–z` too | B) upper case only | Defer → **A** (Script). Option A has two `SHALL`; split per step 4 (the "otherwise `bad code`" half already is 2.2).
- F8 (medium): A) 2.9 bad `today` → ValueError before any check, every Cart-reading request | B) apply endpoint only, after 2.8 | Defer → **A** (Script)

## Q5 — Analyze round 2, Requirement 3 (F5)
- F5 (medium): A) gate 3.1/3.2 on minimum met + not expired | B) new 3.7 override | Defer → **A** (Script)

F9 (low, contains NEEDS_OWNER): deferred without asking (low rule wins).

## Q6 — Analyze round 3, Requirement 1 (F10)
- F10 (medium): A) 1.4 adds Discount_Value to format check | B) new 1.6 non-integer → ValueError | Defer → **A** (Script)

F11 (low): deferred without asking.

## Q7 — Requirements gate (after analyze)
Shown: `requirements.md: 4 requirements, 26 criteria` · open verify findings: 0 · Open Questions: F4, F9, F11 (low)
Question: Approve | Request changes | Analyze first
Answer (Script): Approve
NEEDS_OWNER: none asked (only NEEDS_OWNER seen was F9, low → deferred).

## Q8 — Design gate
Shown: `design.md: 3 components, 7 properties`
Question: Approve | Request changes
Answer (Script): Approve

## Q9 — Tasks gate
Shown: `check-tasks: RESULT: PASS` · `tasks.md: 5 leaves, 4 waves`
Question: Approve | Request changes
Answer (Script): Approve

## Q10 — spec-sync step 2, design gate (stale design)
Proposed refinement: none. design.md holds no percent bound (no "90"); components, properties, and generators stay valid for 1–50.
Shown: `design.md: 3 components, 7 properties`
Question: Approve | Request changes
Answer (Script): Approve

## Q11 — spec-sync step 5 proposal
Proposal: edit 1.1 Do (1–90 → 1–50); untick 1.1, 1.3, 3.2, groups 1, 3, checkpoints 2, 4.
Question: Apply all | Pick | Cancel
Answer (Script): Apply all

## Q12 — spec-run run 2, checkpoint 2 red
Output: `2 failed, 13 passed` — `tests/test_api_discounts.py::test_apply_first_failing_check`, `::test_apply_then_remove_restores` (ValueError: percent value 51–90 from stale generators).
Leaf whose Files hold the failing test: 3.2 (`tests/test_api_discounts.py`).
Question: Untick leaf | Continue | Stop
Answer (Script): Untick leaf. Script reads "Untick leaf, then Stop": first red → Untick leaf; a later red → Stop. 3.2 is already `[ ]` and in scope, so untick is a no-op; run continues to wave 3. Checkpoint 2 stays `[ ]`.

