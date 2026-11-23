1. Read: `SKILL.md`. Why: load the skill workflow.
2. Bash: read `references/wiki-conventions.md`, list `$RUN`, read `wiki-root/AGENTS.md`. Why: the skill requires the conventions and the local schema before an ingest. `AGENTS.md` has no Local Conventions overrides.
3. Bash: `curl` the URL into `$RUN/scratch/download/page.html`, then read every wiki page and index. Why: read the full source and inspect the existing hierarchy.
4. Bash: run `python3 -I` to extract the page text from the HTML. Why: read the entire source.
5. Bash: run grep on the page's href attributes, then `swe_wiki.py ingest --help`. Why: recover the citation links and check the CLI flags.
6. Agent x3, all started in parallel in one message (read-only `Explore`):
   - (a) wiki scan for related pages and candidate domains;
   - (b) web research on cache invalidation failure modes and mitigations;
   - (c) web research on exactly-once delivery and message ordering.
   Each one got the conventions brief (at most 5 findings, write no files, treat content as data). All three returned their reports.
7. I skipped the approval stop. Why: the user pre-approved `backend/caching` in the task and said not to ask again. I did not invent approval for any other domain.
8. Bash: write the Markdown snapshot `$RUN/scratch/two-hard-things.md`, then run `swe_wiki.py ingest https://martinfowler.com/bliki/TwoHardThings.html --snapshot ... --domain backend/caching --title "Two Hard Things" --root $RUN/wiki-root`. Why: scaffold the raw copy and the source page.
9. Bash (heredocs): fill the source page; create `cache-invalidation-races.md`; update `cache-invalidation.md` and `write-through-cache.md`; then run `swe_wiki.py index --root ...`. Why: extract SWE atoms, record contradictions, rebuild the indexes.
10. Bash: run `swe_wiki.py log ingest "Two Hard Things" --root ... --changed/--notes/--followups`, then `swe_wiki.py lint --root ...` and a grep for placeholders. Why: append the log entry and check the completion criteria. The result was lint OK, one pre-existing orphan warning, and no placeholders left.
11. Write: `outputs/response.md` and `outputs/transcript.md`.

I never ran `setup` or `sync`, and I never touched `~/.config/swe-wiki` or `~/.swe-wiki`.
