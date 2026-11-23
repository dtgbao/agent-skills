---
title: "Cache Invalidation"
summary: "Strategies to keep cached data consistent: TTL, write-through, and event-driven purge."
kind: concept
domain: backend/caching
status: draft
tags: [swe, caching]
sources: []
updated: 2026-10-01
confidence: medium
---

# Cache Invalidation

Strategies to keep cached data consistent: TTL, write-through, and event-driven purge.

- Default TTL for read-heavy product data: 300 seconds.
- Prefer event-driven purge when the write path can publish change events.
- See [Write-Through Cache](write-through-cache.md).
