# Payments architecture review, 2026-09-04

Attendees: Mai (payments lead), Omar (SRE), Lena (gateway team)

- Decision: retry calls to the payments gateway at most 3 times, with exponential backoff
  starting at 200 ms. Reason: avoid duplicate charges and gateway overload.
- Idempotency keys are required on every charge request.
- Owner of the gateway client: payments team.
