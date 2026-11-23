I read the cache stampede notes (team sync, 2026-11-10). Nothing is written yet. I need your approval first.

**Proposed domain: `backend/caching`**

- The wiki already owns caching knowledge there: `wiki/backend/caching/cache-invalidation.md` and `wiki/backend/caching/write-through-cache.md`.
- A stampede is a cache-expiry failure mode. It belongs next to TTL and invalidation.
- Alternatives: `backend/reliability` (if you want incident and load-protection patterns kept apart from caching), or `backend/databases/postgres` (not recommended, because Postgres is only the victim).

**Key takeaways**

1. A hot-key expiry sends hundreds of concurrent misses to Postgres. The catalog key expiry at peak raised p99 from 40 ms to 2.3 s.
2. Three mitigations: single-flight (request coalescing), XFetch (probabilistic early expiration), and stale-while-revalidate.
3. Decision: single-flight in the catalog service now. Evaluate XFetch for the pricing service. Owner: platform team.
4. The 300 s TTL stays. This agrees with the 300 s default in `cache-invalidation.md`.

**Planned pages**

- New source page: `wiki/backend/caching/sources/cache-stampede-notes.md`.
- New concept: `cache-stampede.md` (failure mode plus the three mitigations, with a Mermaid flow).
- New decision: `catalog-stampede-single-flight.md` (context, options, decision, consequences, status).
- Update `cache-invalidation.md`: link to the stampede page, and note that a plain TTL alone causes stampedes on hot keys.

**Contradictions with the wiki**

- None. The notes confirm the 300 s TTL for read-heavy product data.

**Web research (already arrived; I will merge it during the write)**

- In-process single-flight dedups only within one process. With N catalog replicas, one expiry can still send about N loads to Postgres. A cross-instance lease (Redis `SET NX PX` with a token-checked release) gives one load per expiry. This limits what the decision buys. ([oneuptime, 2026-01-21](https://oneuptime.com/blog/post/2026-01-21-redis-cache-stampede/view), [Redis stampede guide](https://redis.antirez.com/fundamental/cache-stampede-prevention.html))
- Single-flight failure modes: one slow or failed rebuild hits all waiters. A lock that expires during a slow fetch lets a duplicate fetch start. Do not cache failures. Give waiters one shared timeout.
- XFetch needs a physical TTL longer than the logical 300 s TTL. It takes no lock, so a few parallel refreshes can still occur. It serves briefly stale data, so the pricing team must decide if that is acceptable for prices. (Vattani et al., VLDB 2015)
- TTL jitter spreads expiry across many keys. It does not help one hot key.
- No finding contradicts the 300 s TTL.

**Questions for you**

1. Approve `backend/caching`, or pick an alternative?
2. How many catalog replicas run? If more than one, I will record the cross-instance gap as an open question on the decision page.
3. Anything to emphasize, for example the pricing XFetch evaluation?
