# Scenario briefs

Each session gets: "Read `evals/sdd/harness.md` and follow it. Work only in `evals/sdd/runs/v<version>/<id>/`." plus the brief below. Fixture per scenario: 01/02 `shortlinks`, 03 `pager`, 04 `notes`, 05 `account-auth`, 06 `textkit`, 07 `notes` (07c `pager`).

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

## 07-brainstorm-sonnet

Tests `spec-brainstorm` through `/sdd:spec-new` step 2 (Clarity). Three runs, one session each, ids `07a`, `07b`, `07c`. Stop each run after the workflow gets its first input (before Gate 1). Brainstorm writes no files, so after each run list `WS/docs/specs/` and `git status` in `WS`.

### 07a-vague

Run: `/sdd:spec-new make notes better, people keep losing stuff` (fixture `notes`).

Script (answers to open questions, one per message): "Last week I deleted a note by mistake and it was gone." → why now: "second time this month" → success: "I can get a deleted note back" → non-goal: "no sync, no cloud". Grill rounds: take every `(Recommended)` option, except "keep deleted notes forever" → "purge after 30 days", and surface → "library only". Playback 1 → "Wrong: it must also work from the CLI, not only the library." Playback 2 (corrected) → Confirm. Workflow → take the recommended option. Stop before Gate 1.

Checks: the first reply names the open slots and offers "skip". One open question per message, no option list. Code read (README, `notes/`) before the first question. Grill uses AskUserQuestion, ≤4 questions, recommendation first. Playback ≤300 words, has the full shape, marks guesses `(guess)`. Correction → new playback before step 3. Confirmed playback → name and workflow options use it. Brainstorm writes no file and changes no code. Before `requirements.md`, only `.spec.json` from `SPEC init` exists.

### 07b-clear

Run: `/sdd:spec-new Requirements-First: add a "tag" subcommand to the notes CLI so a user can attach one or more tags to a note by id and filter "list" by tag. Done when "list --tag X" shows only notes with tag X. Out: tag colors.` (fixture `notes`).

Script: none expected. A question → log it, answer "none", mark `UNSCRIPTED`.

Checks: verdict = clear. Output = a one-line brief, all five slots filled. Zero questions before the workflow Context step. No playback, no grill round. Name step runs next, then the named workflow. Brief slots match the input (no invented non-goal).

### 07c-defect

Run: `/sdd:spec-new Bugfix: paginate(items, 3, 10) returns an empty page for 25 items` (fixture `pager`).

Script: Facts step. Repro as in the run line → "25 items, size 10, page 3" · current "empty page, total_pages is 2" · expected "page 3 has 5 items, total_pages is 3" · must hold "exact multiples work; page < 1 and size < 1 raise ValueError".

Checks: Clarity step makes no brief and asks no open question. Brainstorm is skipped (or ends at once with "defect report"). Bugfix `Facts` step (`bugfix.md` workflow step 1) asks only the missing facts, ≤4 questions. Facts the input implies appear in the Introduction without a question. No `spec-brainstorm` playback.

### 07 pass criteria

| Run | PASS when |
|---|---|
| 07a | All 07a checks hold. Playback confirmed in chat before any spec file exists. Workflow chosen from the playback. |
| 07b | Zero questions. One-line brief shown. |
| 07c | Brainstorm skipped. Facts step asks. |

Scenario PASS = 07a, 07b and 07c PASS. Any file written by brainstorm = FAIL. Report one `report.md` per run; log plugin issues as `07-<n>`.

