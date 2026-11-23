---
title: Payments gateway
kind: entity
domain: team/payments
summary: The external card-payments gateway that the payments team calls for every charge.
tags: [payments]
sources: [raw/team/payments/2026-09-arch-review.md]
created: 2026-09-05
updated: 2026-09-05
---

# Payments gateway

The external service that processes card charges. The payments team owns the client.
Calls follow the [retry policy](retry-policy.md) ([review](2026-09-arch-review.md)).
