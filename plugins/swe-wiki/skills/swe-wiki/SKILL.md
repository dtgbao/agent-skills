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
| Ingest | Read one source fully, propose its primary domain, wait for approval, scaffold its source page, extract SWE knowledge, rebuild local indexes, then append a log entry. |
| Query | Start at `wiki/index.md`, follow domain indexes, search for recall, answer with citations, and file reusable synthesis in its owning domain when it should compound. |
| Migrate | Preview an explicit domain-assignment manifest, obtain approval, then apply it only from a clean Git worktree. |
| Lint | Run mechanical lint, repair drift, then perform the semantic checks in the conventions reference. |
| Sync | Explicitly commit wiki changes, rebase onto the current remote branch, and push without force. |

## Init

`init` is local, idempotent, and Git-independent:

```bash
python3 <script> init
python3 <script> init --root <wiki-root>
```

`init` never rearranges a legacy kind-first wiki. If it reports a legacy layout, use the migration workflow before ingesting new material.

## Ingest

Use one source at a time unless the user explicitly asks for batch ingestion.

Before creating, copying, or editing anything:

1. Read the entire source and inspect the existing domain indexes and related pages.
2. Recommend one lowercase, kebab-case primary domain such as `aws/iam`. Explain why it owns the knowledge, identify related existing pages, and offer reasonable alternative domains when they exist.
3. Wait for explicit user approval. For cross-domain material, choose one canonical primary domain and use tags and cross-links for secondary discovery; never duplicate the page.
4. Pass the approved domain to the CLI. Supplying `--domain` asserts that approval was obtained.

```bash
python3 <script> ingest <source-path-or-url> --domain aws/iam --title "Source title"
python3 <script> ingest <transcript-path> --asset <slide-path> --domain aws/iam --title "Source title"
```

The script copies local source files and repeated `--asset` files into `raw/<domain>/` without moving or overwriting their originals. URLs remain external provenance. It creates the source-page scaffold under `wiki/<domain>/sources/`; durable synthesis pages belong directly under `wiki/<domain>/` and keep their page kind in frontmatter.

Extract every software-engineering atom worth keeping: architecture decisions, tradeoffs, invariants, failure modes, interfaces, data flows, algorithms, testing strategy, security/reliability/performance notes, deployment details, best practices, code conventions, commands, and reusable principles.

Update existing pages instead of creating near-duplicates. Create a page only when its concept, decision, blueprint, practice, convention, or system will be useful independently. Architecture decisions and blueprints should include Mermaid diagrams when relationships, flows, or boundaries matter.

Complete ingestion only when every changed page appears in its local `index.md`, ancestor indexes reach that domain, `wiki/log.md` has a parseable `ingest` entry, and contradictions or superseded claims are recorded on the affected pages.

## Migrate

Migration is explicit and never automatic. Create a JSON manifest that assigns every legacy wiki page and flat raw file to one approved primary domain:

```json
{
  "assignments": [
    {
      "domain": "aws/iam",
      "paths": [
        "wiki/systems/aws-identity-and-access-management.md",
        "wiki/sources/2026-07-28-iam-introduction.md",
        "raw/2026-07-28-iam-introduction.txt"
      ]
    }
  ]
}
```

Preview first and show the exact moves and indexes to the user:

```bash
python3 <script> migrate <manifest.json>
```

Wait for explicit approval, verify the dedicated wiki Git worktree is clean, then apply:

```bash
python3 <script> migrate <manifest.json> --apply
```

Application moves files, adds domain frontmatter, rewrites relative links and provenance, removes emptied legacy kind directories, rebuilds indexes, and appends a `migrate` log entry. Do not sync unless the user separately requests it.

## Query

Start with the root domain index, follow the most relevant nested indexes, then search:

```bash
python3 <script> query "question or keywords"
```

Answer from wiki pages first and cite page paths. Read raw sources only when the wiki points there or the index is insufficient. If the answer creates reusable synthesis, save it under the owning domain with `kind: question`, rebuild its indexes, and append a `query` log entry.

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
python3 <script> log migrate "Domain-first wiki layout"
```
