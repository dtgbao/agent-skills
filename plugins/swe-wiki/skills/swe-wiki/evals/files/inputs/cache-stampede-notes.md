# Cache stampede notes (team sync, 2026-11-10)

When a hot key expires, hundreds of requests miss at once and all hit Postgres.
Last week the product catalog key expired at peak and p99 latency went from 40 ms to 2.3 s.

Options we discussed:
1. Request coalescing (single-flight): one request rebuilds, others wait on it.
2. Probabilistic early expiration (XFetch): refresh before TTL with rising probability.
3. Stale-while-revalidate: serve stale value, refresh in background.

Decision: use single-flight in the catalog service now, evaluate XFetch for the pricing service.
Our 300 s TTL stays. Owner: platform team.
