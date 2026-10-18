# QA log

## spec-analyze round 1

Repairs before asking (step 3):
- F6: A (decline/fail) and B (timeout) close different gaps → split into F6a (A only) and F6b (B only, renamed A). Each now has one non-NEEDS_OWNER option → ask A | Defer.
- F7: one option, not NEEDS_OWNER → ask A | Defer.
- F9: low → deferred without asking.

### Call 1 — Requirement 1
| Q | Options | Answer | Source |
|---|---|---|---|
| F6a (medium, FAILURE): Payment_Provider declines or fails the charge? | A) 1.3: IF the Payment_Provider declines or fails the charge, THEN … HTTP 402 `payment_failed`, create no Gift_Card · Defer | A | Script: high/medium → A |
| F6b (medium, FAILURE): Payment_Provider does not answer? | A) 1.x: IF no answer within 10 seconds, THEN … HTTP 504 `payment_timeout`, create no Gift_Card · Defer | A | Script: high/medium → A |
| F7 (medium, EDGE): purchase value outside 10–500 or not whole? | A) 1.4: … HTTP 400 `invalid_amount`, no charge · Defer | A | Script: high/medium → A |

### Call 2 — Requirement 2
| Q | Options | Answer | Source |
|---|---|---|---|
| F3 (medium, AMBIGUITY): "promptly" | A) within 2 s for 95% · B) within 500 ms for 99% · Defer | A | Script |
| F4 (medium, INCONSISTENCY): 500 vs 1000 dollar limit | A) 2.3 up to 500 dollars · B) 1.1 buy 10–1000 · Defer | A | Script |
| F5 (high, EDGE): subtotal > balance | A) 2.5 balance → 0, return amount due · B) 2.5 409 `insufficient_balance` · Defer | A | Script |
| F8 (medium, EDGE): concurrent redemptions | A) 2.6 serialize, balance never < 0 · B) 2.6 409 `card_busy` · Defer | A | Script |

### Call 3 — Requirements 3, 4
| Q | Options | Answer | Source |
|---|---|---|---|
| F1 (medium, NEEDS_OWNER): What is Merchant_Portal, and which route, method, and staff credential sends a void request? | A) NEEDS_OWNER answer · Defer | Most conservative concrete value: no Merchant_Portal component; staff void through Shop_API route `POST /gift-cards/<code>/void`; caller must have `ctx["actor"]["role"] == "staff"`; any other caller → HTTP 403 `forbidden`. | Script: NEEDS_OWNER → most conservative concrete value (logged) |
| F2 (high, INCONSISTENCY): never expire vs 12-month void | A) 4.1 keep balance unchanged until voided under 3.1 or 4.2 · B) 4.2 SHALL NOT change status for unused time · Defer | A | Script |

## spec-analyze round 2

Repairs: F10 and F11 each have one non-NEEDS_OWNER option → ask A | Defer.

### Call 4 — Requirements 2, 4
| Q | Options | Answer | Source |
|---|---|---|---|
| F11 (medium, INCONSISTENCY): 2.1 vs 2.5 when subtotal > balance | A) 2.1 limited to subtotal ≤ balance · Defer | A | Script |
| F10 (high, INCONSISTENCY): 4.1 "unchanged" vs redemption | A) 4.1 unchanged except by redemption under 2.1/2.5, so … · Defer | A | Script |

## spec-analyze round 3

### Call 5 — Requirement 5
| Q | Options | Answer | Source |
|---|---|---|---|
| F12 (high, NEEDS_OWNER): What `ctx` Payment_Provider call undoes a charge (name, arguments, failure result)? | A) NEEDS_OWNER answer · Defer | Most conservative concrete value: `ctx["payment_provider"].refund(charge_id)`; `charge_id` is the value `ctx["payment_provider"].charge(amount_cents)` returned; refund raises an exception on failure. On ledger failure during creation, refund the charge. | Script: NEEDS_OWNER → most conservative concrete value (logged) |

## spec-analyze VERIFY 1 (one Resolve + Apply)

Repairs: F14 one option with two assertions → ask A | Defer, split at apply. F15 one option → ask A | Defer.

### Call 6 — Requirements 1, 3
| Q | Options | Answer | Source |
|---|---|---|---|
| F16 (medium, NEEDS_OWNER): After `payment_timeout`, how must a late successful charge be undone with no `charge_id`? | A) NEEDS_OWNER answer · Defer | Most conservative concrete value: Shop_API makes its own `charge_ref` before the charge, sends it as `charge(amount_cents, charge_ref)`, and on timeout calls `refund(charge_ref)`. `refund` takes the same `charge_ref`. | Script: NEEDS_OWNER → conservative value (logged) |
| F13 (medium, NEEDS_OWNER): Which `ctx` key holds actor role and id? | A) NEEDS_OWNER answer · Defer | Most conservative concrete value: `ctx["actor"] = {"id": str, "role": "shopper" \| "staff"}`; a missing `ctx["actor"]` counts as not `staff`. | Script: NEEDS_OWNER → conservative value (logged) |
| F15 (medium, EDGE): void of unknown code | A) 3.4 404 `unknown_card` · Defer | A | Script |

### Call 7 — Requirement 5
| Q | Options | Answer | Source |
|---|---|---|---|
| F14 (medium, FAILURE): refund raises during 5.3 | A) 5.4 503 `refund_failed` + error log · Defer | A | Script |

## spec-new (resume)

| Q | Options | Answer | Source |
|---|---|---|---|
| `docs/specs/gift-cards/` exists. Resume or new name? | Resume · New name | Resume | Script |

Resume point: `SPEC drift` → NO DRIFT. First phase in `order` not `approved` = `design`.

### Gate — design
Shown: `docs/specs/gift-cards/design.md: 4 components, 9 properties` (analyze ran: criteria 12 → 23).

| Q | Options | Answer | Source |
|---|---|---|---|
| Approve design? | Approve · Request changes | Approve | Script: every gate Approve |

### Gate — tasks
`SPEC check-tasks` → RESULT: PASS (1 WARN: checkpoint 4 runs after later-layer leaf 5.1, shared wave).
Shown: `docs/specs/gift-cards/tasks.md: 5 leaves, 4 waves`.

| Q | Options | Answer | Source |
|---|---|---|---|
| Approve tasks? | Approve · Request changes | Approve | Script: every gate Approve |

Then told user: `/sdd:spec-run gift-cards`.

