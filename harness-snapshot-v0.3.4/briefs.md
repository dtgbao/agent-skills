# Scenario briefs

Each session gets: "Read `plugins/sdd/evals/harness.md` and follow it. Work only in `docs/sdd-eval/v<version>/<id>/`." plus the brief below. Fixture per scenario: 01/02 `shortlinks`, 03 `pager`, 04 `notes`, 05 `account-auth`, 06 `textkit`.

## 01-reqfirst-sonnet / 02-reqfirst-haiku (same script)

Run: `/sdd:spec-new Requirements-First: add per-API-key rate limiting to the shortlinks API. 60 requests per minute per key. Over the limit return 429 with a Retry-After header in seconds.`

Script: Gate 1 → "Analyze first" (high/med → A, low → Defer), then Approve. Gate 2 → "Request changes: inject the clock so tests control time; name the window algorithm (fixed or sliding) and why", then Approve. Gate 3 → Approve. Stop before spec-run.

Checks: spec-new can dispatch spec-analyst? `.spec.json` per gate. Graph validator script. Word counts. Skeleton fit. (02 adds: instructions hard for a small model.)

## 03-bugfix-sonnet

Run: `/sdd:spec-new Bugfix: the last page of results is missing when the item count is not a multiple of the page size. With 25 items and size 10, paginate(items, 3, 10) returns an empty page and total_pages is 2.` then `/sdd:spec-run <name> --mode single`.

Script: must-hold facts = exact multiples work; page < 1 and size < 1 raise ValueError; empty list → 0 pages. Gates → Approve. Leaves → Run; failure → Retry once, then Stop.

Checks: exploration red before fix, preservation green before fix, all green after. Root cause `file:line`. Which design Done-when items fit the bugfix skeleton. Effect of `*` on pins. Leftover `[-]`.

## 04-designfirst-haiku

Run: `/sdd:spec-new Design-First: add an "export" subcommand to the notes CLI that writes all notes to Markdown or JSON. Follow the fixed architecture in README.md.`

Script: Level → Low-Level. Gates → Approve. "Which user needs does this architecture miss?" → "export one note by id (`--id N`) and write to a file path (`--out PATH`)".

Checks: how the late answer is applied; stale rule after step 7; visuals usage; graph validator.

## 05-analyze-haiku

Seeded spec `account-auth`, all phases approved. Run: `/sdd:spec-analyze account-auth`. Script: high/med → A, low → Defer.

Answer key (secret from the analyst): K1 password 8–64 vs 6–64 · K2 "quickly" · K3 never expire vs 30 min idle · K4 "Tenant"/support role not in Glossary · K5 duplicate email · K6 Mailer down · K7 unknown-email reset, expired link · Req 7 = clean control.

Checks: recall/precision per round, severity, format, EARS of edits, Open Questions, stale marking, rounds.

## 06-lifecycle-sonnet

Run: `/sdd:spec-new Quick Plan: add slugify(title) and unique_slug(title, existing) to textkit ... max 50 chars ...` → `/sdd:spec-run <name> --mode waves --optional` → hand edit requirements 50 → 40 (no `.spec.json` change) → `/sdd:spec-sync <name>` → `/sdd:spec-run <name> --mode waves --optional`.

Script: ASCII via NFKD, empty → "untitled", existing is set[str], Hypothesis. Approve all. Failures → Retry once, then Skip. Checkpoint red → Stop. Counterexample → fix implementation. Sync → Apply all.

Checks: one-message wave dispatch, disjoint files, `[-]` reverts, property tags and iterations, hand-edit detection, sync matrix, spec-run routing, typecheck absent.
