---
name: swe-wiki
description: SWE wiki maintainer for a persistent, Git-synced software engineering knowledge base. Use when setting up, ingesting, querying, linting, or syncing a markdown wiki for architecture decisions, blueprints, best practices, and code conventions.
---

# SWE Wiki

Maintain a persistent, compounding markdown wiki for software engineering knowledge. Raw sources are immutable; the wiki is the LLM-owned synthesis layer.

Resolve `scripts/swe_wiki.py` relative to this `SKILL.md` before running it. The examples below use `<script>` for that resolved absolute path.

## First Use

If no configured, initialized wiki exists, start setup before any ingest, query, lint, or sync:

1. Ask where to persist the wiki, offering `~/.swe-wiki` as the default. Wait for the answer.
2. Ask for the existing Git repository URL used to synchronize the wiki. Recommend a private repository because the wiki may contain proprietary information. Wait for the answer.
3. Run setup non-interactively with both answers:

```bash
python3 <script> setup --root <wiki-root> --repo <git-repository>
```

Do not request or embed Git credentials. Setup relies on the user's existing Git or SSH authentication. When a person runs `setup` directly in a terminal, the script provides interactive prompts for omitted values.

Setup stores the selected root in `~/.config/swe-wiki/config.json`. Commands resolve the root from an explicit `--root`, then this config, then `~/.swe-wiki`.

## Routing

Read `references/wiki-conventions.md` before initializing a wiki, ingesting a source, making durable query output, or repairing lint failures.

| Branch | Action |
| --- | --- |
| Setup | Configure this computer, clone or initialize the dedicated Git repository, initialize the wiki, make the initial commit when needed, and push. |
| Init | Create or repair the local wiki structure without configuring or invoking Git. |
| Ingest | Read one source fully, scaffold its source page, extract SWE knowledge, update durable pages and `index.md`, then append a log entry. |
| Query | Read `index.md`, search for recall, read relevant pages, answer with citations, and file reusable synthesis under `wiki/questions/` when it should compound. |
| Lint | Run mechanical lint, repair drift, then perform the semantic checks in the conventions reference. |
| Sync | Explicitly commit wiki changes, rebase onto the current remote branch, and push without force. |

## Init

`init` is local, idempotent, and Git-independent:

```bash
python3 <script> init
python3 <script> init --root <wiki-root>
```

## Ingest

Use one source at a time unless the user explicitly asks for batch ingestion.

```bash
python3 <script> ingest <source-path-or-url> --title "Source title"
```

The script creates the source-page scaffold. Read the entire source, including code blocks, diagrams, tables, footnotes, and referenced local images when available, then write the synthesis.

Extract every software-engineering atom worth keeping: architecture decisions, tradeoffs, invariants, failure modes, interfaces, data flows, algorithms, testing strategy, security/reliability/performance notes, deployment details, best practices, code conventions, commands, and reusable principles.

Update existing pages instead of creating near-duplicates. Create a page only when its concept, decision, blueprint, practice, convention, or system will be useful independently. Architecture decisions and blueprints should include Mermaid diagrams when relationships, flows, or boundaries matter.

Complete ingestion only when `wiki/index.md` lists every added or changed page, `wiki/log.md` has a parseable `ingest` entry, and contradictions or superseded claims are recorded on the affected pages.

## Query

Start with the index, then search:

```bash
python3 <script> query "question or keywords"
```

Answer from wiki pages first and cite page paths. Read raw sources only when the wiki points there or the index is insufficient. If the answer creates reusable synthesis, save it as `wiki/questions/<slug>.md`, update `index.md`, and append a `query` log entry.

## Lint

Run the mechanical linter:

```bash
python3 <script> lint
```

Then perform the semantic lint: contradictions, stale claims, missing cross-links, important concepts without pages, weak source provenance, and architecture pages missing useful diagrams.

Complete lint only when mechanical errors are fixed or reported, semantic findings are fixed or listed as follow-ups, and `wiki/log.md` has a parseable `lint` entry.

## Sync

Synchronize only when the user explicitly requests it:

```bash
python3 <script> sync
```

Sync stages and commits all changes in the dedicated wiki repository, fetches and rebases the current branch, and pushes it. It never force-pushes. If rebase conflicts occur, it aborts the rebase, preserves the local commit, and reports the conflicting files. Stop for user-guided resolution; do not resolve or force-push automatically.

Git history is the sync audit trail. Do not append sync events to `wiki/log.md`.

## Log

Append workflow entries after the corresponding agent-led work:

```bash
python3 <script> log ingest "Article Title"
python3 <script> log query "Cache invalidation comparison"
python3 <script> log lint "Monthly wiki health check"
```
