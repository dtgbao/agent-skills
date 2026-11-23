# Git and GitHub

The wiki root is one Git repository: `AGENTS.md`, `raw/` and `wiki/`.

## Setup

1. Ask the user for the wiki root and the URL of an **existing** repository.
2. Recommend a private repository. Wiki pages and raw sources can hold private notes,
   meeting content and personal data. Example: `gh repo create my-wiki --private`.
3. Accept these URL forms: `git@github.com:owner/repo.git`, `https://github.com/owner/repo.git`,
   `ssh://git@github.com/owner/repo.git`. A local path or `file://` URL also works.
4. The CLI refuses URLs with credentials (`user:token@`, `ghp_...`, `?access_token=`).
   Tell the user to authenticate with SSH keys, `gh auth login` or a credential helper.

```bash
python3 <skill-dir>/scripts/llm_wiki.py setup --remote git@github.com:me/my-wiki.git --root ~/.llm-wiki --json
```

- Empty root and a remote with commits: the CLI clones it.
- Empty remote: the CLI runs `git init` and adds `origin`.
- Existing repository at the root: the CLI checks that `origin` matches.

The config goes to `~/.config/llm-wiki/config.json`: `root`, `remote`, `branch`.

## Sync

Run sync only when the user asks. Sync writes no `log.md` entry; Git history records it.

```bash
python3 <skill-dir>/scripts/llm_wiki.py lint
python3 <skill-dir>/scripts/llm_wiki.py sync -m "Ingest IAM policy evaluation guide" --json
```

Sync does: `git add -A`, commit when there are changes, `git pull --rebase`, `git push`.
It never force-pushes.

## The schema is always tracked

`sync` adds `AGENTS.md` with `git update-index`, which bypasses ignore rules. So a
global ignore file that lists `AGENTS.md` cannot drop the schema.

## Conflicts

The CLI resolves conflicts in generated files by itself and continues the rebase:

| File | Resolution |
|---|---|
| `wiki/log.md` | Keep every entry of both sides once. Remote order stays; local entries go in time order. |
| `index.md` files | Regenerate from the merged pages. |

The JSON lists these files in `resolved`.

Exit code 2 and `error.code: rebase-conflict` mean that another file also conflicts.
The CLI already ran `git rebase --abort`. The local commit is kept and nothing was pushed.

1. Report the files in `conflicts` to the user.
2. Ask how to resolve them. Typical choices: merge both versions of a page by hand,
   or keep one side.
3. Never force-push, `reset --hard` or rewrite history to get past a conflict.
