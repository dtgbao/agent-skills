I ingested "Two Hard Things" (Martin Fowler, 2009, last revised 2021) under `backend/caching`, the domain you approved.

## What changed

| File | Change |
| --- | --- |
| `raw/backend/caching/two-hard-things.md` | Immutable Markdown snapshot of the page. The URL stays as provenance. |
| `wiki/backend/caching/sources/2026-11-23-two-hard-things.md` | New source page: summary, SWE extraction, impacted pages, related reading, open questions. |
| `wiki/backend/caching/cache-invalidation-races.md` | New concept page: stale-set race (Mermaid sequence), fill-vs-invalidation reordering, concurrent puts, stampedes, and a mitigation table. |
| `wiki/backend/caching/cache-invalidation.md` | Added "Why It Is Hard" with the Karlton citation, plus notes on TTL and purge. |
| `wiki/backend/caching/write-through-cache.md` | Added a tension note: concurrent `put`s can race. |
| Indexes, `wiki/log.md` | Rebuilt the indexes and appended an `ingest` entry. |

## Key takeaways

1. The source is an aphorism and makes no technical argument. Its value is as the canonical citation that cache invalidation is hard.
2. Invalidation is hard because events race. A late fill can overwrite a purge and stay stale forever (Facebook NSDI 2013; Meta 2022).
3. Mitigations: invalidate with `delete`, gate fills with leases or versions, keep a TTL only as a staleness bound, and measure how far the cache drifts from the store.
4. Riffs on the quote: off-by-one errors, plus exactly-once delivery and message ordering in distributed systems.

## Contradictions recorded

- `write-through-cache.md` vs. delete-on-write: Facebook invalidates with `delete`, because two writers that `put` can leave the older value in cache.
- `cache-invalidation.md` has a 300-second default TTL. Meta's research treats TTL as a freshness model, not a consistency fix. I kept the default and labeled it a backstop.

## Not done (needs your decision)

- **Exactly-once delivery and message ordering:** this knowledge does not belong in caching. The sources are in Related Reading. I can create a page under `backend/distributed-systems` if you approve that domain.
- **Naming things:** no page yet. A candidate domain is `software-design/naming`.
- **Unverified figures:** the NSDI 2013 lease figures come from MIT course notes, because I could not read the paper text. Confidence on those is medium.
- **Lint:** it passes. It warns about one orphan page, `wiki/aws/iam/least-privilege.md`, which existed before this ingest.
- **Sync:** I did not sync. Say "sync" when you want to commit and push.
