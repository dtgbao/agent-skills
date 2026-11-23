I ingested "Two Hard Things" (Martin Fowler, 2009, revised to 2021) into `backend/caching`, as you approved.

**Files**

| File | Change |
| --- | --- |
| `raw/backend/caching/two-hard-things.md` | New. Immutable Markdown snapshot of the URL. |
| `wiki/backend/caching/sources/2026-11-23-two-hard-things.md` | New source page: summary, SWE extraction, related reading, open questions. |
| `wiki/backend/caching/cache-invalidation.md` | Added "Why It Is Hard", failure modes (stale set, thundering herd) with a sequence diagram, and mitigations (leases, invalidate on write, stampede control). |
| `wiki/backend/caching/write-through-cache.md` | Added a Contradictions section. |
| Indexes, `wiki/log.md` | Rebuilt indexes. Appended an `ingest` entry. |

**Key takeaways**

- Karlton's quote names cache invalidation and naming as the two hard things.
- The riffs add off-by-one errors, exactly-once delivery, and message ordering.
- The attribution has no primary document. The earliest dated online trace is Tim Bray, 2005.
- The source is folk wisdom. Most technical depth on the cache page comes from web research. I marked it medium-low confidence.

**Contradiction to review**

The write-through page says "reads stay fresh". Web research (Redis blog) prefers deleting the key on write over updating it. Concurrent writes can leave a stale cache value. I recorded this on the page. I did not change its guidance.

**Not done, needs your choice**

- Naming things and exactly-once delivery have no home domain. Pick domains if you want pages for them, for example `software-engineering/naming` and `distributed-systems/messaging`.
- Follow-up source candidate: "Scaling Memcache at Facebook" (NSDI 2013), for leases.

Lint passes. One warning is unrelated: `wiki/aws/iam/least-privilege.md` is an orphan. I did not run sync. Ask me if you want to push.
