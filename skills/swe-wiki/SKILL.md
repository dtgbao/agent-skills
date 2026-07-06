---
name: swe-wiki
description: SWE wiki maintainer for a persistent software engineering knowledge base. Use when ingesting engineering sources, querying accumulated software knowledge, linting wiki health, or bootstrapping a markdown wiki for architecture decisions, blueprints, best practices, and code conventions.
---

# SWE Wiki

Maintain a persistent, compounding markdown wiki for software engineering knowledge. The raw sources are immutable; the wiki is the LLM-owned synthesis layer.

## Routing

First locate the wiki root. If none exists, ask for the target directory or initialize one with:

```bash
python skills/swe-wiki/scripts/swe_wiki.py init <wiki-root>
```

Read `references/wiki-conventions.md` before bootstrapping a wiki, ingesting a source, making durable query output, or repairing lint failures.

| Branch | Action |
| --- | --- |
| Bootstrap | Create the root structure, `wiki/index.md`, `wiki/log.md`, and page directories with the `init` command. |
| Ingest | Read the source fully, scaffold a source page with `ingest`, extract SWE knowledge, update durable pages, update `index.md`, then append a log entry. |
| Query | Read `index.md` first, run `query` for recall, read relevant pages, answer with citations, and file reusable synthesis under `wiki/questions/` when it should compound. |
| Lint | Run `lint`, fix mechanical drift, then do the semantic checks in `references/wiki-conventions.md`. |

## Ingest

Use one source at a time unless the user explicitly asks for batch ingestion.

```bash
python skills/swe-wiki/scripts/swe_wiki.py ingest <wiki-root> <source-path-or-url> --title "Source title"
```

Extract every software-engineering atom worth keeping: architecture decisions, tradeoffs, invariants, failure modes, interfaces, data flows, algorithms, testing strategy, security/reliability/performance notes, deployment details, best practices, code conventions, commands, and reusable principles.

Update existing pages instead of creating near-duplicates. Create new pages only when the concept, decision, blueprint, practice, convention, or system will be useful independently. Architecture decisions and blueprints should include Mermaid diagrams when relationships, flows, or boundaries matter.

Complete ingestion only when `wiki/index.md` lists every added or changed page, `wiki/log.md` has a parseable `ingest` entry, and contradictions or superseded claims are recorded on the affected pages.

## Query

Start with the index, then search:

```bash
python skills/swe-wiki/scripts/swe_wiki.py query <wiki-root> "question or keywords"
```

Answer from wiki pages first and cite page paths. Read raw sources only when the wiki points there or the index is insufficient. If the answer creates reusable synthesis, save it as `wiki/questions/<slug>.md`, update `index.md`, and append a `query` log entry.

## Lint

Run the mechanical linter:

```bash
python skills/swe-wiki/scripts/swe_wiki.py lint <wiki-root>
```

Then perform the semantic lint: contradictions, stale claims, missing cross-links, important concepts without pages, weak source provenance, and architecture pages missing useful diagrams.

Complete lint only when mechanical errors are fixed or reported, semantic findings are either fixed or listed as follow-ups, and `wiki/log.md` has a parseable `lint` entry.

## Log

Append workflow entries with:

```bash
python skills/swe-wiki/scripts/swe_wiki.py log <wiki-root> ingest "Article Title"
python skills/swe-wiki/scripts/swe_wiki.py log <wiki-root> query "Cache invalidation comparison"
python skills/swe-wiki/scripts/swe_wiki.py log <wiki-root> lint "Monthly wiki health check"
```
