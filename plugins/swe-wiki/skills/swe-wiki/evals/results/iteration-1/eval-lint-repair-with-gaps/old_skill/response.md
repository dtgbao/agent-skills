# SWE Wiki Health Check

**Result:** Mechanical lint passes (`OK`). One warning is left. I fixed 3 items. 5 items need your input.

## Fixed

| Item | Change |
| --- | --- |
| Placeholder summary | `wiki/backend/caching/cdn-caching.md` showed `_Fill during ingestion._` in the index. I wrote a summary from the page's own content. |
| Orphan page | `cdn-caching.md` had no inbound links. I cross-linked it with `cache-invalidation.md`, in both directions. |
| Unnamed contradiction | I added an "Open Tensions" section to both caching pages. It records the TTL conflict. I did not choose a value. |

I rebuilt the indexes and added a `lint` entry to `wiki/log.md`.

## Needs Your Input

1. **TTL conflict.** Both pages give a default TTL for read-heavy product data. `cache-invalidation.md` says 300 s. `cdn-caching.md` says 60 s. Which value is correct? They can both be correct if they apply to different layers (origin and edge). If so, I will state that on both pages.
2. **No provenance.** All 4 pages have `sources: []`, and `raw/` contains no files. Can you give me the source documents? I can then ingest them and cite them. Otherwise, should I lower `confidence` on `least-privilege.md` from `high`?
3. **Orphan: `wiki/aws/iam/least-privilege.md`.** No other page links to it. No related page exists yet. Do you want to add IAM material, or accept the warning?
4. **No Git repository.** The wiki root is not a Git working tree. `sync` cannot run. Do you want to run `setup` with a private remote?
5. **Duplicate log entries.** `wiki/log.md` has repeated `bootstrap | SWE wiki initialized` entries. The index rebuild added one more. The log is append-only, so I did not remove them. Tell me if you want them cleaned up.

## Suggested Pages

- `stale-while-revalidate` and event-driven purge appear in the caching pages. Neither has its own page. Add them when a source supports them.

Nothing is committed or synced.
