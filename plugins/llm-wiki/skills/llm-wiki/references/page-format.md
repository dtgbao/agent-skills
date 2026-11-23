# Page format

## Frontmatter

Every page starts with this block. The CLI parses a small YAML subset: `key: value`,
inline lists `[a, b]` and block lists (`- item`). Quote values that contain `:` or `#`.

```yaml
---
title: IAM policy evaluation
kind: concept
domain: aws/iam
summary: How AWS combines identity, resource and SCP policies into one allow or deny.
tags: [security, aws/organizations]
sources: [raw/aws/iam/policy-eval-guide.html, raw/aws/iam/policy-eval-guide.md]
created: 2026-11-23
updated: 2026-11-23
---
```

| Field | Required | Rule |
|---|---|---|
| `title` | yes | Human title. The index link text. |
| `kind` | yes | A generic kind or an extra kind from the AGENTS.md marker |
| `domain` | yes | Equals the page's folder under `wiki/` |
| `summary` | yes | One plain sentence, 160 characters or fewer. No links or Markdown. The index shows it as is. |
| `tags` | no | Secondary domains and topics |
| `sources` | no | Raw paths (`raw/...`) or URLs. The index shows the count. Lint checks that raw paths exist. |
| `created`, `updated` | `updated` yes | `YYYY-MM-DD`. Set `updated` on every change. |
| `source_url`, `retrieved` | source pages | Set by `ingest` |

Never derive the summary from the body. Write it on purpose.

## Kinds and body sections

| Kind | Use for | Suggested sections |
|---|---|---|
| `overview` | The map and synthesis of one domain | Current picture, Key pages, Open questions |
| `source` | One raw source | Source, Summary, Key takeaways, Entities and concepts, Contradictions and open questions |
| `entity` | A named thing: product, tool, person, organization | What it is, Facts (cited), Relations, History |
| `concept` | An idea, mechanism or term | Definition, How it works, Examples, Related |
| `decision` | A choice | Context, Options, Decision, Rationale, Status, Consequences |
| `practice` | A how-to or rule of thumb | When to use, Steps, Pitfalls |
| `question` | A question and its answer | Question, Answer, Evidence, Open points |

A preset or the user can add kinds in `AGENTS.md`. Follow the sections it defines.

## Links and citations

- Use relative Markdown links: `[Policy types](policy-types.md)`,
  `[SCP](../organizations/scp.md)`. No wiki-link syntax, so any viewer works.
- Cite claims inline: `Explicit deny wins ([guide](iam-policy-evaluation-guide.md)).`
- Link to raw files when a reader needs the original:
  `[original](../../../raw/aws/iam/policy-eval-guide.html)`. Lint does not check links
  outside `wiki/`.
- Do not link to `index.md` files from pages. Indexes are generated.

## Files and names

- File name: kebab-case slug of the title, `.md`.
- Never edit `index.md` by hand. Never edit or reorder `log.md`; only append with `log`.
- Write `TODO(llm-wiki)` only as a placeholder that you will replace. Lint fails on it.
