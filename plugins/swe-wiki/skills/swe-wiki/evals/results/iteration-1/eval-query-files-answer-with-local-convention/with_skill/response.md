**Use event-driven purge for the product catalog. Keep the 300-second TTL as a backstop.**

Here is what the wiki says:
- `wiki/backend/caching/cache-invalidation.md` sets a 300-second default TTL for read-heavy product data. It also prefers event-driven purge when the write path can publish change events.
- `wiki/backend/caching/write-through-cache.md` uses write-through for read-after-write data, such as user profiles. Write-through adds latency to every write.

A product catalog is read-heavy, so it does not need write-through's per-write cost.

| Factor | Write-through | Event-driven purge |
| --- | --- | --- |
| Freshness after a write | Immediate on the writer's path | After the event is consumed. The TTL caps staleness. |
| Write latency | Higher | Low |
| Fits | Read-after-write data (user profiles) | Read-heavy product data |
| Needs | One owned write path | A write path that publishes change events |
| Main risk | Cache and store drift apart when a write fails partway | A lost event leaves stale data until the TTL expires |

**When the answer changes:**
- If the catalog write path cannot publish events, use TTL only, or write-through for that path.
- If editors must see their own edits at once, add write-through or a cache bypass for the editor path only.

**Gaps:** Neither cited page links to a raw source (`sources: []`). The wiki also has no data on catalog write volume or event delivery guarantees. Treat this recommendation as medium confidence.

**Saved to the wiki:**
- New: `wiki/backend/caching/product-catalog-write-through-vs-event-purge.md` (`kind: question`). Following your wiki's local conventions, it has the `team-platform` tag and ends with a 4-item `## Decision Checklist`.
- Updated: `wiki/backend/caching/cache-invalidation.md` now links to the new page.
- Rebuilt the indexes and added a `query` entry to `wiki/log.md`.
- Lint passes. It shows one older warning that is not from this change: `wiki/aws/iam/least-privilege.md` has no inbound links.

I did not sync. Ask me if you want to commit and push.
