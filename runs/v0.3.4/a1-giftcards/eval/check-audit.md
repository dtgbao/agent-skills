# CHECK line audit (M3)

Rule (spec-analyze step 3): CHECK missing or not `gaps=1 shall=1 asserts=1` → repair. I also re-count each option myself; a self-report that is wrong counts as a fail.

## Round 1
| Finding | CHECK present | Self-report | Orchestrator count | Result | Repair |
|---|---|---|---|---|---|
| F1 | yes | 1/1/1 | A: shall=1, asserts=1 + removes 4.2 (supersede). B: asserts=2 ("balance unchanged" + "can be reinstated") | FAIL (B) | B: drop "and the card can be reinstated" before asking. A: 4.2 removal logged as supersede. |
| F2 | yes | 1/1/1 | 1/1/1 | pass | — |
| F3 | yes | 1/1/1 | 1/1/1 (409 + unchanged = one rejection outcome) | pass | — |
| F4 | yes | 1/1/1 | 1/1/1 | pass | — |
| F5 | yes | 1/0/0 owner=sole | NEEDS_OWNER, sole option | literal FAIL (not `shall=1 asserts=1`) | none possible: a NEEDS_OWNER option has no SHALL. Treated as pass. Plugin rule gap (see report). |
| F6 | yes | 1/1/1 | gaps=2: A closes "declined", B closes "any failure" (covers unavailable too) | FAIL | split: F6a (decline, A) and F6b (non-decline failure, B narrowed to "for a reason other than a decline") |
| F7 | yes | 1/1/1 | 1/1/1 | pass | — |
| F8 | yes | 1/1/1 | A: asserts=2 (refund + create no Gift_Card) | FAIL | "create no Gift_Card" is covered by 5.2 (change rejected) → drop at apply, log |
| F9 | yes | 1/1/1 | 1/1/1 | pass | — |

Round 1: 9/9 CHECK present. 4 fail (F1, F5 literal, F6, F8). 3 repaired; F5 needs no repair.

## Round 2
| Finding | CHECK present | Self-report | Orchestrator count | Result | Repair |
|---|---|---|---|---|---|
| F12 | yes | 1/0/0 owner=sole | NEEDS_OWNER, one gap | literal FAIL only | none needed |
| F13 | yes | 1/0/0 owner=sole | gaps=2 (missing actor; creation old value) | FAIL | split: F13a (missing actor), F13b (old value on creation) |

Round 2: 2/2 CHECK present. 2 literal fails; 1 real fail (F13) repaired by split.

## Round 3
| Finding | CHECK present | Self-report | Orchestrator count | Result | Repair |
|---|---|---|---|---|---|
| F16 | yes | 1/1/1 | asserts=2 ("active until void" + "no elapsed time changes … balance") | FAIL | drop "so no elapsed time changes the status or balance"; keep "with no expiry date" |

## VERIFY 1
| Finding | CHECK present | Self-report | Orchestrator count | Result | Repair |
|---|---|---|---|---|---|
| F17 | yes | 1/1/1 | 1/1/1 | pass | — |
| F18 | yes | 1/1/1 | 1/1/1 | pass | — |

## VERIFY 2
| Finding | CHECK present | Self-report | Orchestrator count | Result | Repair |
|---|---|---|---|---|---|
| F19 | yes | 1/1/1 | 1/1/1 | pass | none (→ Open Questions) |
| F20 | yes | 1/1/1 | 1/1/1 | pass | none (→ Open Questions) |

## Totals
- Findings from analyst: 20 analyst-numbered (F1–F9, F12, F13, F16–F20) = 16 analyst findings; F10, F11, F14, F15 came from the orchestrator cross-check (no CHECK line expected).
- CHECK line present: 16/16.
- Fail by the literal step-3 rule (`gaps=1 shall=1 asserts=1`): 7 (F1, F5, F6, F8, F12, F13, F16). Of these, 2 are NEEDS_OWNER only (F5, F12): `shall=0 asserts=0` is correct for an owner question, nothing to repair.
- Real fails: 5 (F1, F6, F8, F13, F16). All 5 had a self-report that said pass or that missed a second gap; the orchestrator's own count caught them. All 5 repaired (narrow, split, or drop clause).
