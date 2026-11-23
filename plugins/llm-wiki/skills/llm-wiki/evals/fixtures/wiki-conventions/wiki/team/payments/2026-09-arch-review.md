---
title: Payments architecture review 2026-09-04
kind: source
domain: team/payments
summary: Review that set the gateway retry limit to 3 and made idempotency keys mandatory.
tags: [payments]
sources: [raw/team/payments/2026-09-arch-review.md]
created: 2026-09-05
updated: 2026-09-05
---

# Payments architecture review 2026-09-04

## Source

- [raw/team/payments/2026-09-arch-review.md](../../../raw/team/payments/2026-09-arch-review.md)

## Summary

The team limited gateway retries to 3 with exponential backoff and required idempotency
keys on every charge.

## Key takeaways

- At most 3 retries, backoff from 200 ms ([retry policy](retry-policy.md)).
- Idempotency keys on every charge request.

## Entities and concepts

- [Payments gateway](payments-gateway.md)

## Contradictions and open questions

- None found.
