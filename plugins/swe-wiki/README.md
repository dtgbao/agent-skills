# SWE Wiki Plugin

Maintain a persistent Markdown knowledge base for software engineering decisions, blueprints, practices, conventions, systems, and reusable answers. The wiki lives in a dedicated Git repository so it can be synchronized safely across computers.

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
- `ingest`: Read a source and synthesize reusable engineering knowledge.
- `query`: Search the wiki and answer with page citations.
- `lint`: Check mechanical structure and semantic health.
- `sync`: Explicitly commit, rebase, and push without force.

Synchronization is never automatic. If a rebase conflicts, the script aborts it, preserves the local commit, and reports the files requiring user-guided resolution.

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
