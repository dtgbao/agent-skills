# LLM Wiki Plugin

An agent plugin, bundling the `llm-wiki` skill, that turns sources into a persistent, interlinked Markdown wiki in a Git
repository. It implements Andrej Karpathy's
[LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):
the agent reads each source once and integrates it into existing pages. It does not
re-derive knowledge on every question.

It works with any agent host that can read Markdown and run a shell command: Claude Code,
Codex, Cursor, Copilot, Devin and others. It has no dependency on Obsidian, qmd, Marp
or Dataview.

## Layout of a wiki

```text
~/.llm-wiki/                 # one Git repository (private recommended)
├── AGENTS.md                # per-wiki schema; the agent reads it before every operation
├── raw/<domain>/            # immutable sources, URL snapshots, assets/
└── wiki/
    ├── index.md             # generated catalog (never edit by hand)
    ├── log.md               # append-only: ## [YYYY-MM-DD HH:MM] <op> | <title>
    └── <domain>/            # e.g. aws/iam: pages + generated index.md
```

## Install

Claude Code:

```text
/plugin marketplace add dtgbao/agent-skills
/plugin install llm-wiki@bao-plugins
```

GitHub Copilot:

```bash
copilot plugin marketplace add dtgbao/agent-skills
copilot plugin install llm-wiki@bao-plugins
```

Codex:

```bash
codex plugin marketplace add dtgbao/agent-skills
codex plugin add llm-wiki@bao-plugins
```

Hosts without plugin support: point the agent at `skills/llm-wiki/SKILL.md` in your
instructions file.

## CLI

`skills/llm-wiki/scripts/llm_wiki.py` is one Python 3.9+ file with no dependencies. Every command takes
`--root PATH` and `--json`.

| Command | What it does |
|---|---|
| `setup --remote URL` | Connect the root to an existing repository. Refuses credentials in the URL. |
| `init [--preset P] [--domain D]` | Create the layout and AGENTS.md. Logs `bootstrap`. |
| `ingest SRC --domain D [--snapshot] [--asset F]` | Copy or snapshot into `raw/`, scaffold a source page |
| `index` | Rebuild every `index.md` from the `summary:` fields. No log entry. |
| `search "Q"` | BM25 search, title ×3, summary ×2, tags ×2 |
| `log OP "TITLE"` | Append a log entry (bootstrap, ingest, query, lint, schema) |
| `lint [--strict]` | Placeholders, frontmatter, summaries, links in `wiki/`, orphans, log, raw refs |
| `sync [-m MSG]` | Commit, `pull --rebase`, push. Aborts the rebase on conflict. Never forces. |
| `status` | Root, remote, counts, recent log, lint totals |

Config: `~/.config/llm-wiki/config.json`. Default root: `~/.llm-wiki`.

## Development

```bash
cd skills/llm-wiki
python3 -m unittest discover -s tests -v
uvx ruff check . && uvx ruff format --check . && uvx ty check .
```

Tests use a temporary HOME, temporary roots, local bare Git remotes and `file://` URLs.
They make no network calls.

Evals live in `skills/llm-wiki/evals/`: `evals.json` lists the prompts and assertions;
`fixtures/` holds the fixture wikis and sources; `grade.py` grades a finished run directory.
