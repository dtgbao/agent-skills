---
name: web-search
description: Use when web search is needed for current technical docs, version-specific implementation guidance, library setup, or web-grounded summaries.
---

# Web Searcher

Use web search to ground technical answers in current, relevant sources.

## Defaults

Apply these defaults unless the user explicitly overrides them:

- Prefer **official documentation first**.
- Use maintainer-authored release notes, migration guides, GitHub discussions, or issues next.
- Use community sources only as fallback or to fill gaps.
- Default `max number of sources` to **5**.
- Include **sample code** unless the user says not to.
- Return output in **Markdown**.

## Input handling

When the user asks for technical implementation help, infer or extract these fields:

- `topic`: the implementation question or task
- `framework/version`: explicit version if provided; otherwise infer the likely current version carefully and call out uncertainty
- `max number of sources`: user-provided or default 5
- `include code examples`: yes/no; default yes
- `output format`: Markdown

If the request is ambiguous, do not stop. Make a best effort search using the clearest interpretation, then note any ambiguity in the caveats section.

## Search workflow

Follow this sequence:

1. Identify the core technology, version, and implementation task.
2. Search for **official docs** using a minimal query first.
3. Search maintainer sources for the same task when official docs leave gaps.
4. Search broader community sources only if authoritative sources conflict, omit practical details, or lack concrete examples.
5. Open the most relevant pages and verify:
   - version alignment
   - publication or last-updated signals when available
   - whether the content is actually about the requested framework/version
6. Prefer newer, version-matching sources over older generic ones.
7. Discard stale or low-confidence sources when a stronger source is available.
8. Synthesize the answer instead of copying source text.

## Source ranking rules

Rank sources in this order:

1. Official product or framework documentation
2. Official migration guides, release notes, or maintainer docs
3. Maintainer-authored blog posts, GitHub discussions, or GitHub issues
4. Third-party blogs, tutorials, forum posts, and Q&A threads

When sources conflict, prefer the highest-ranked source that clearly matches the requested version.

## Recency rules

For every answer:

- Explicitly check for version and freshness clues.
- Mention the freshest useful signal you found, such as:
  - documentation page update date
  - framework version in the docs URL or title
  - release or migration guide date
  - the date of a community answer if it is being relied on
- If freshness is unclear, say so plainly.
- If the user asked for the **latest** information, make recency a core part of the answer rather than a footnote.

## Output

Use `references/output-template.md` when formatting the final answer or needing the worked example. Skip it only when the user asks for a different shape.

## Writing rules

- Be concise and practical.
- Do not overwhelm the user with every source you found.
- Respect the user-provided source limit.
- If official docs fully answer the question, keep community sources minimal.
- If no authoritative source exists, say that clearly and explain what you relied on.
- Preserve nuance around version differences.
- Never invent APIs, config keys, CLI flags, or version support.
