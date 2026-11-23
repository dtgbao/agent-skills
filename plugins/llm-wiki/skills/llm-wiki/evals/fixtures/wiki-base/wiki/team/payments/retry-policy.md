---
title: Gateway retry policy
kind: decision
domain: team/payments
summary: Retry payments gateway calls at most 3 times with exponential backoff from 200 ms.
tags: [payments, reliability]
sources: [raw/team/payments/2026-09-arch-review.md]
created: 2026-09-05
updated: 2026-09-05
---

# Gateway retry policy

## Context

Gateway timeouts caused duplicate charges in the past.

## Decision

Retry at most **3** times, exponential backoff starting at 200 ms. Every charge carries an
idempotency key ([review](2026-09-arch-review.md)).

## Status

Accepted, 2026-09-04.
