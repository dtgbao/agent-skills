# Scripted Q&A

## Q1 — spec-new / gate.md step 2 (requirements gate)
Shown: `requirements.md: 4 requirements, 18 criteria`
Question: Approve this artifact?
Options: Approve | Request changes | Analyze first (Recommended: money domain)
Answer: Analyze first (Script: requirements gate, first "Analyze first")

## spec-analyze step 3 repair (round 1)
- F5 option A closes 3 gaps (Minimum_Subtotal, Expiry_Date, Discount_Kind) → split into F5a (1.6), F5b (1.7), F5c (1.8). Each has one option, not NEEDS_OWNER → ask A | Defer.
- F2 A and F3 A both target new 2.6 → F3 keeps 2.6, F2 becomes 2.7.
- F7 low → deferred without asking.

## Q2 — spec-analyze step 3, Requirement 1 (call 1 of 3)
- F5a (medium): A) 1.6 reject Minimum_Subtotal not integer ≥0 | Defer → **A** (Script: high/medium → A)
- F5b (medium): A) 1.7 reject Expiry_Date not real `YYYY-MM-DD` date | Defer → **A**
- F5c (medium): A) 1.8 reject Discount_Kind not `percent`/`fixed` | Defer → **A**

## Q3 — spec-analyze step 3, Requirement 2 (call 2 of 3)
- F2 (medium): A) 2.7 check order 400,404,410,422,409 | B) order 400,409,404,410,422 | Defer → **A**
- F3 (medium): A) 2.6 bad-format string → 400 `bad code` | B) → 404 `unknown code` | Defer → **A**
- F6 (medium, NEEDS_OWNER): Which ctx keys give `handle` the Code_Registry and the Clock, and what is the Clock signature? → **`ctx["codes"]` = Code_Registry; `ctx["clock"]` = zero-arg callable returning the current UTC `datetime.date`.** (Script: NEEDS_OWNER → most conservative concrete value. Rationale: follows the existing `ctx` dict pattern; injected clock = no hidden wall-clock reads.)

## Q4 — spec-analyze step 3, Requirements 3–4 (call 3 of 3)
- F1 (medium): A) 3.2 same code re-apply → 200 only if unexpired and minimum met | B) 200 without re-check | Defer → **A**
- F4 (medium): A) 4.6 Subtotal below minimum → Discount_Amount 0 | B) keep discount | Defer → **A**

## spec-analyze step 3 repair (round 2)
- F9 option A has two assertions ("set Discount_Amount to 0" and "keep the Applied_Code attached"). EARS rule: one observable assertion → split A into 4.7 + 4.8. B left as is.

## Q5 — spec-analyze step 3, Requirements 2 and 4 (round 2)
- F8 (medium): A) 2.8 unknown cart → 404 `no cart` before any other check | B) after the 400 check | Defer → **A**
- F9 (medium): A) 4.7 expired Applied_Code → Discount_Amount 0; 4.8 Applied_Code stays attached | B) discount unchanged | Defer → **A**

## spec-analyze step 3 repair (round 3)
- F10 option A keeps two assertions ("return 409" and "keep the Applied_Code") → split: 3.1 = 409; new 3.4 = Applied_Code unchanged.
- F10 option B only restates the 2.7 text with a "so that" clause (no rule change). Shown as is.

## Q6 — spec-analyze step 3, Requirement 3 (round 3)
- F10 (high): A) 3.1 409 only for a different code that passes 400/404/410/422 checks (+3.4 keep code) | B) 2.7 restated | Defer → **A** (Script: high → A)

## spec-analyze step 5 result
Growth 18 → 28 criteria (+55.6 %). >50 % → skill says recommend splitting the spec. Recommendation shown: split Requirement 1 (code registry) into its own spec. No question asked by the skill; kept as one spec (Script has no split step).

## Q7 — gate.md step 1–2 after Analyze (requirements gate, second pass)
Shown: `requirements.md: 4 requirements, 28 criteria (18 → 28)`; open verify findings: none.
Options: Approve | Request changes | Analyze first
Answer: **Approve** (Script: "Then Approve")

## Q8 — gate.md step 2 (design gate)
Shown: `design.md: 3 components, 8 properties`
Options: Approve | Request changes
Answer: **Approve** (Script: design gate → Approve)

## Q9 — gate.md step 2 (tasks gate)
`check-tasks` → RESULT: PASS (2 WARN: checkpoints 2 and 4 share waves with later-layer leaves 3.1, 5.1).
Shown: `tasks.md: 6 leaves, 4 waves`
Options: Approve | Request changes
Answer: **Approve** (Script: tasks gate → Approve)
Then told user: `/sdd:spec-run discount-codes`.

## Q10 — spec-run step 6 / correctness.md step 5 (counterexample, leaf 1.2, Property 2)
Shown: shrunk input first=('0','percent',1,0,'2000-01-01'); second register('0','percent',0,0,'') raised InvalidCode, not DuplicateCode.
Options: fix implementation | fix test | fix requirement
Answer: **fix implementation** (Script: Counterexample → fix implementation)
Note: the runner had already weakened its own test (runner step 3 allows it; correctness.md step 5 says the test stays unchanged until the user picks). Action: re-dispatch leaf 1.1 with the fix (duplicate check right after Code_String check), then re-dispatch leaf 1.2 to restore Property 2 as written ("any fields").
