**Recommendation: use event-driven purge for the product catalog, with the 300 s TTL as a backstop.** This holds only if the catalog write path can publish change events.

Why, from your wiki:

- `wiki/backend/caching/cache-invalidation.md` sets a 300 s default TTL for read-heavy product data.
- The same page prefers event-driven purge when the write path can publish change events.
- `wiki/backend/caching/write-through-cache.md` says write-through costs write latency. It scopes write-through to read-after-write consistency on user profile data, not catalog data.

| Factor | Write-through | Event-driven purge |
| --- | --- | --- |
| Write latency | Higher | Lower (async purge) |
| Read-after-write | Strong | Short stale window |
| Fit for read-heavy product data | Weak | Strong (wiki default) |
| Precondition | One write path owns cache and store | Write path publishes change events |

If the write path cannot publish events, the wiki has no rule. Then pick TTL-only, or write-through if catalog editors need read-after-write consistency.

Confidence is medium. Both cited pages have no raw sources (`sources: []`).

**Saved to the wiki:**

- New page: `wiki/backend/caching/product-catalog-write-through-vs-event-driven-purge.md` (`kind: question`). It follows your local `AGENTS.md` rules: tag `team-platform` and a closing `## Decision Checklist` with 5 items.
- Cross-links added from `cache-invalidation.md` and `write-through-cache.md`.
- Indexes rebuilt: `wiki/backend/caching/index.md`, `wiki/backend/index.md`, `wiki/index.md`.
- `query` entry appended to `wiki/log.md`. The index rebuild (`init`) also appended a `bootstrap` entry.
- Lint passes. One existing warning: `wiki/aws/iam/least-privilege.md` is an orphan.

I did not sync. Say "sync the wiki" to commit and push.
