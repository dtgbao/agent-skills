I read the cache stampede notes in full. I checked the wiki. I did not write anything yet.

**Recommended primary domain: `backend/caching`**

Why this domain owns the notes:
- The notes cover a cache failure mode (stampede on hot-key expiry) and three mitigations.
- `backend/caching` already holds the related pages. No new top-level domain is necessary.

Related existing pages:
- `wiki/backend/caching/cache-invalidation.md`: it sets a 300 s default TTL for read-heavy product data. The notes keep the 300 s TTL. I will link the stampede risk from this page.
- `wiki/backend/caching/write-through-cache.md`: this page is related, but the notes do not change it.

Alternative domains:
- `backend/caching/stampede`: a subdomain, if you expect more stampede material.
- `backend/reliability`: a new domain, if you file stampedes as a reliability failure mode.

Planned changes after you approve:
1. Copy the notes to `raw/backend/caching/`. The original file stays in place.
2. Create a source page under `wiki/backend/caching/sources/`.
3. Create `cache-stampede.md` (concept). It covers the failure mode, the incident (p99 went from 40 ms to 2.3 s), and the three options: single-flight, XFetch, stale-while-revalidate.
4. Create `catalog-cache-stampede-mitigation.md` (decision). It records single-flight for the catalog service now, XFetch evaluation for pricing, the 300 s TTL, and the platform team as owner. It includes a Mermaid sequence diagram.
5. Update `cache-invalidation.md` with a cross-link and the stampede note.
6. Rebuild the indexes and add an `ingest` entry to `wiki/log.md`.

Do you approve `backend/caching`? You can also pick an alternative domain.
