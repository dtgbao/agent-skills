# SWE Wiki Plugin

Maintain a persistent, domain-first Markdown knowledge base for software engineering decisions, blueprints, practices, conventions, systems, and reusable answers. The wiki lives in a dedicated Git repository so it can be synchronized safely across computers.

## Install

Add this repository as a Codex marketplace, then install the bundled plugin:

```bash
codex plugin marketplace add dtgbao/agent-skills
codex plugin add swe-wiki@bao-plugins
```

Start a new Codex task after installation so the bundled skill is available.

## First Use

Ask Codex to set up the SWE wiki. It will ask for:

1. A local wiki directory, defaulting to `~/.swe-wiki`.
2. An existing Git repository used for synchronization.

Use a private repository when the wiki may contain proprietary information. Authentication remains managed by Git or SSH; do not put credentials in the repository URL.

Setup clones an existing repository or initializes an empty one, creates the wiki structure, saves the local root in `~/.config/swe-wiki/config.json`, and performs the initial push.

## Workflows

- `init`: Create or repair a local wiki without invoking Git.
- `ingest`: Classify a source into an approved primary domain, preserve local inputs under `raw/<domain>/`, and synthesize reusable engineering knowledge.
- `migrate`: Preview and explicitly apply a legacy kind-first to domain-first migration.
- `query`: Search the wiki and answer with page citations.
- `lint`: Check mechanical structure and semantic health.
- `sync`: Explicitly commit, rebase, and push without force.

Synchronization is never automatic. If a rebase conflicts, the script aborts it, preserves the local commit, and reports the files requiring user-guided resolution.

## Domain Layout

Knowledge is organized by the technical domain that owns it, not by page kind or source course structure:

```text
wiki/
├── index.md
└── aws/
    ├── index.md
    └── iam/
        ├── index.md
        ├── durable-page.md
        └── sources/
            ├── index.md
            └── source-page.md
raw/
└── aws/
    └── iam/
        └── source-files
```

The root index links top-level domains; every nested wiki directory has its own local index. Page kind remains frontmatter metadata. Before ingestion, Codex reads the source, recommends a primary domain and alternatives, and waits for approval.

The CLI requires that approved domain explicitly:

```bash
python3 skills/swe-wiki/scripts/swe_wiki.py ingest ./lesson.txt \
  --asset ./slide.png \
  --domain aws/iam \
  --title "IAM lesson"
```

Legacy migrations use a JSON assignment manifest and preview by default. Apply only after reviewing the exact moves:

```bash
python3 skills/swe-wiki/scripts/swe_wiki.py migrate ./migration.json
python3 skills/swe-wiki/scripts/swe_wiki.py migrate ./migration.json --apply
```

## Requirements

- macOS or Linux
- Python 3
- Git with user-managed authentication and commit identity

The implementation uses only the Python standard library and the `git` executable.

## Development

Run the isolated test suite:

```bash
python3 -m unittest discover -s plugins/swe-wiki/tests -v
```
