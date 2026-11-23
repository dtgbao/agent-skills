The wiki health check is done. Mechanical lint now passes with 0 errors. One warning is left.

## What I fixed

| Issue | Fix |
| --- | --- |
| **ERROR:** `wiki/backend/caching/cdn-caching.md` still had a `_Fill during ingestion._` placeholder | I replaced it with a summary paragraph. I wrote it only from the bullets already on the page. |
| **WARN:** `cdn-caching.md` had no `summary` in its frontmatter | I added a one-line summary. The caching index now shows it. |
| **WARN:** `cdn-caching.md` was an orphan page | I linked it from `cache-invalidation.md` and linked back. |
| **Semantic:** the two pages disagreed on TTL and did not say so | I added an "Open Tensions" note to both pages. I did not choose a value. |

After that, I rebuilt the indexes and added a `lint` entry to `wiki/log.md`. I changed only `cdn-caching.md`, `cache-invalidation.md` and `wiki/backend/caching/index.md`.

## What needs your input

1. **TTL conflict.** The two pages give different TTLs for read-heavy product data:
   - `cdn-caching.md` says 60 s.
   - `cache-invalidation.md` says 300 s.

   Which value is correct? Or does each value apply to a different layer (CDN edge vs. origin cache)? If they are per-layer, I will reword both pages to say so.
2. **No sources.** All 4 pages have `sources: []`. `least-privilege.md` is marked `confidence: high` but cites nothing. Can you give me sources to ingest? If not, should I lower its confidence to `medium`?
3. **Orphan page.** `wiki/aws/iam/least-privilege.md` has no links from other pages, and no other page covers a related topic. It can stay as it is until you add more IAM pages. Or I can add a planned Access Analyzer page that links to it.
4. **Duplicate log entries.** `wiki/log.md` has the same bootstrap entry 3 times. The log is append-only, so I did not remove them. Tell me if you want them removed anyway.
5. **No Git.** `wiki-root` is not a Git working tree, so `sync` cannot run. To connect it to your private repository, you need to run setup.

## Gaps (also recorded as follow-ups in the log)

- Question: what is the longest that data can stay stale when you add the CDN TTL to the origin TTL?
- Source to find: the AWS IAM Access Analyzer documentation, and maybe a page for it.
- Possible new pages: event-driven purge, and `stale-while-revalidate`.

The wiki has no decision or blueprint pages, so no pages were missing diagrams.
