I ingested "Two Hard Things" (Martin Fowler, 2009, last revised 2021) into `backend/caching`. You approved that domain.

**Changed**

- `wiki/backend/caching/sources/2026-11-23-two-hard-things.md` - new source page. It covers provenance, a summary, extracted points, impacted pages, and open questions.
- `wiki/backend/caching/cache-invalidation.md` - new section, "Why Invalidation Needs Explicit Design". It cites the source, and the source is now in its frontmatter.
- The indexes are rebuilt: `wiki/index.md`, `wiki/backend/index.md`, `wiki/backend/caching/index.md` and `wiki/backend/caching/sources/index.md`.
- `wiki/log.md` - new `ingest | Two Hard Things` entry.

**Notes**

- The source is a URL, so it stays as external provenance. Nothing went into `raw/`.
- The article is a short anecdote, not a technical guide. Its main point is the Phil Karlton saying: cache invalidation and naming are the two hard things. The attribution has no primary source. The earliest trace is a Tim Bray post from 2005.
- I did not create new durable pages. The article gives no technique that deserves its own page. No contradictions with existing pages.
- To refresh index summaries after editing, I ran `init`. That also added an extra `bootstrap` entry to `wiki/log.md`. The log is append-only, so I left the entry in place.
- Lint passed. One warning existed before this ingest: `wiki/aws/iam/least-privilege.md` is an orphan.

**Follow-ups for you**

- Choose a domain for naming conventions, for example `software-engineering/naming` or `api-design`.
- Choose a domain for messaging guarantees (exactly-once delivery, ordering), for example `distributed-systems/messaging`.

I did not sync. Tell me when you want me to run sync.
