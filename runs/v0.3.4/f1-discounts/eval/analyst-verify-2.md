# Analyst VERIFY 2 (5.6, 5.7) — raw hand-back from agent a61c8f54e2cd29bba

```
ID: F11
TYPE: INCONSISTENCY
SEVERITY: medium
AFFECTS: Requirement 5.6
QUOTE: "THEN THE Handler SHALL answer status 500 with body `{"error": "bad_context"}` before any body check."
ISSUE: 5.6 fixes the order against body checks only. `shop/api.py` returns 404 `{"error": "no cart"}` for an unknown cart id. A request with both a bad context and an unknown cart id has no defined status.
OPTIONS:
  A) 5.8: IF a request to a route in Requirement 5 has a bad context and an unknown cart id, THEN THE Handler SHALL answer status 500 with body `{"error": "bad_context"}`, not 404.
  B) 5.8: IF a request to a route in Requirement 5 has an unknown cart id and a bad context, THEN THE Handler SHALL answer status 404 with body `{"error": "no cart"}`, not 500.
CHECK: gaps=1 shall=1 asserts=1 owner=none

No other defects found from 5.6 and 5.7. 5.7 holds with 5.6. It only constrains Cart lines and Attached_Code, and 5.6 makes the 500 come before any attach or detach.
```

CHECK audit: F11 passes literally and in fact (one SHALL, one assertion).
Disposition: spec-analyze step 5 allows one Resolve+Apply after VERIFY, then one more VERIFY; "findings left → `## Open Questions`". F11 → Open Questions (medium, deferred). Design must decide it.
