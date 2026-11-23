1. Read `SKILL.md` to learn the Query workflow.
2. Bash: read `references/wiki-conventions.md`, because the skill requires it before durable query output. In the same call, listed the wiki files and read `wiki-root/AGENTS.md` for Local Conventions. Found two: question pages need the `team-platform` tag, and they must end with a `## Decision Checklist` of 3-5 checkboxes.
3. Bash: read `wiki/index.md` → `backend/index.md` → `backend/caching/index.md`, then both caching pages and `log.md`. Ran `swe_wiki.py query "write-through event-driven purge product catalog" --root $RUN/wiki-root` for recall.
4. Bash: ran `swe_wiki.py log --help` to check the log options.
5. Bash: wrote the question page `wiki/backend/caching/product-catalog-write-through-vs-event-purge.md`, following the local conventions. Added a cross-link and updated the date on `cache-invalidation.md`. Ran `index --root`, `log query ... --root` and `lint --root`. Lint printed OK, plus one older orphan warning for `wiki/aws/iam/least-privilege.md`.
6. Bash: wrote `outputs/response.md` and this transcript.

Subagents: none. The Query workflow does not ask for any, and this wiki is small. I did not run setup or sync. No scratch files were needed.
