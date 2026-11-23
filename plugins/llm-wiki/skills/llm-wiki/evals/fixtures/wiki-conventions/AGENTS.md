# Wiki schema

The rules of this wiki.

## Layers

- `raw/<domain>/`: immutable sources. Never edit, move, rename or delete a file here.
- `wiki/<domain>/`: pages about the sources.
- `AGENTS.md`: this schema.

## Domains

- A domain is a path of lowercase kebab-case segments, for example `aws/iam`.
- Store each page under exactly one domain. Use tags and links for other domains.
- Every wiki directory has a generated `index.md`. Never edit it by hand.

## Page kinds

- `overview`: the map of a domain and its current synthesis.
- `source`: one raw source: what it says, takeaways, contradictions.
- `entity`: a named thing (product, person, organization, tool).
- `concept`: an idea, mechanism or term.
- `decision`: a choice, its options, rationale and status.
- `practice`: a how-to or rule of thumb, with when to use it.
- `question`: a question that was asked, with the answer and citations.

<!-- llm-wiki:extra-kinds:  -->

## Frontmatter

Every page starts with this block. `summary` is one line of 160 characters
or fewer.

```yaml
---
title: Page title
kind: concept
domain: area/topic
summary: One plain sentence that says what the page covers.
tags: [tag-one, other-domain/topic]
sources: [raw/area/topic/file.md]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Local conventions

- 2026-10-01: Name every question page file with the prefix `q-` (for example `q-why-x.md`).
- 2026-10-01: End every question page with a `## Confidence` section: one word (high, medium or low), then one sentence of reason.
