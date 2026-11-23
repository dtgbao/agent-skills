I read `cache-stampede-notes.md` (team sync, 2026-11-10). I also checked your wiki and searched the web. I have not written anything yet. I need your approval first.

## Recommended domain: `backend/caching`

- This domain already exists. It holds `cache-invalidation.md` and `write-through-cache.md`.
- The notes are about cache behaviour on a hot-key expiry. That is caching knowledge, not Postgres or service knowledge.
- Alternatives:
  - `backend/caching/resilience`: a new subdomain. I do not recommend it yet, because the domain has only 2 pages.
  - `backend/reliability`: use this if you file stampede protection under load protection, not under caching.
- Secondary tags: `postgres`, `performance`, `reliability`.

## Key takeaways

1. **Failure mode:** when a hot key expires, hundreds of concurrent misses go to Postgres. On the catalog key at peak, p99 went from 40 ms to 2.3 s.
2. **Three mitigations:** single-flight (request coalescing), XFetch (probabilistic early expiration) and stale-while-revalidate.
3. **Decision:** use single-flight in the catalog service now. Evaluate XFetch for the pricing service. The platform team owns this.
4. **Invariant:** the 300 s TTL stays.

## Related wiki pages

- `wiki/backend/caching/cache-invalidation.md`: it already sets a 300 s TTL for read-heavy product data, so the notes confirm it. That page does not cover the stampede risk of a fixed TTL. I will add that note and a link.
- `wiki/backend/caching/write-through-cache.md`: this topic is only near the notes. I will add a "See also" link only.
- The wiki has no page on stampede, single-flight, XFetch or SWR yet.

## Notable external findings (for Related Reading)

- **Single-flight is per process.** With N pods, one expiry still sends up to N queries. To coalesce across the fleet, you need a distributed lock or leases, as in Facebook's memcache (NSDI 2013).
- **Single-flight waits need a bound.** In Go, use `DoChan` with a timeout. The first caller's cancellation can fail every waiter. One Postgres error goes to all waiters. Old `x/sync` versions hung after a panic (golang/go#41133).
- **XFetch does not handle cold misses.** It does nothing after a cold start, an eviction or a flush. It also needs the recompute time (`delta`) stored with each value. Start with beta = 1.
- **The Redis TTL must be longer for XFetch.** With XFetch, 300 s becomes the logical expiry, and the physical Redis TTL must be longer.
- **SWR needs a staleness bound.** RFC 5861 adds a stale window on top of the fresh period. nginx (`proxy_cache_lock` plus `use_stale updating`) and Varnish grace pair it with coalescing. SWR is a poor fit for data that must be current on every read.

## Possible contradictions and tensions

- **Single-flight alone:** the notes imply that single-flight stops the stampede. The sources say it stops the stampede only per instance. Waiters still pay the full rebuild latency.
- **Hard 300 s TTL:** keeping it with no early refresh or stale window still lets a stampede happen at the moment of expiry.
- **Pricing:** the notes do not say if pricing can serve stale data. The answer decides between XFetch and SWR.

## Proposed changes

- Create `wiki/backend/caching/cache-stampede.md`: a concept page with a Mermaid flow.
- Create `wiki/backend/caching/catalog-single-flight-decision.md`: a decision record.
- Create the source page and update `cache-invalidation.md`.
- Rebuild the indexes and add an ingest log entry.

**Do you approve `backend/caching`?** Also, what do you want me to emphasize? Two options: the catalog decision record, or the general stampede-mitigation comparison. Do you want the pricing staleness question recorded as an open follow-up?
