---
name: web-search
description: search the web for the latest implementation guidance, official documentation, stack overflow answers, and supporting technical references, then synthesize them into a structured markdown answer with key steps, sample code, source links, recency notes, and confidence caveats. use when a user asks for the latest docs, current implementation guidance, framework or library setup instructions, version-specific coding help, or a concise web-grounded summary for a technical topic.
---

# Web Searcher

Use the available web search tool to find recent, relevant technical guidance and turn it into a concise, well-structured Markdown answer.

## Defaults

Apply these defaults unless the user explicitly overrides them:

- Prefer **official documentation first**.
- Use **Stack Overflow** as the next-choice source for practical implementation details.
- Use **blogs, forums, GitHub issues, or community posts** only as fallback or to fill gaps.
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
3. Search for **Stack Overflow** coverage for the same task.
4. Search broader web sources only if the first two leave gaps, conflict, or lack concrete examples.
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
3. Stack Overflow answers that match the requested version or recent practice
4. Maintainer-authored blog posts, GitHub discussions, or GitHub issues
5. Third-party blogs, tutorials, and forum posts

When sources conflict, prefer the highest-ranked source that clearly matches the requested version.

## Recency rules

For every answer:

- Explicitly check for version and freshness clues.
- Mention the freshest useful signal you found, such as:
  - documentation page update date
  - framework version in the docs URL or title
  - release or migration guide date
  - the date of a Stack Overflow answer if it is being relied on
- If freshness is unclear, say so plainly.
- If the user asked for the **latest** information, make recency a core part of the answer rather than a footnote.

## Output requirements

Always return Markdown using this structure unless the user asks for something else:

# [topic]

## Key steps

- Short, actionable implementation steps in recommended order
- Prefer 4 to 8 bullets

## Sample code

- Include only if `include code examples` is yes
- Keep the example minimal but runnable or directly adaptable
- Match the requested framework and version as closely as possible

## Source links

1. [Title](URL) — one-line reason this source was used
2. [Title](URL) — one-line reason this source was used

## Last updated / recency note

- State the best recency evidence you found
- Note version alignment or uncertainty

## Confidence / caveats

- State confidence as high, medium, or low
- Mention conflicts, ambiguity, or missing official guidance

## Writing rules

- Be concise and practical.
- Do not overwhelm the user with every source you found.
- Respect the user-provided source limit.
- If official docs fully answer the question, keep community sources minimal.
- If no authoritative source exists, say that clearly and explain what you relied on.
- Preserve nuance around version differences.
- Never invent APIs, config keys, CLI flags, or version support.

## Example requests

- Find latest info on how to implement unit test in Nuxt v4.
- Show the current recommended way to configure Vitest in Vue 3.5.
- Summarize the latest docs for Next.js server actions with code examples.
- Compare the latest official guidance for React 19 forms and the top Stack Overflow solution.

For the output template and a worked example, see [references/output-template.md](references/output-template.md).
