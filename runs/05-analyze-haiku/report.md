# 05-analyze-haiku

Model: Haiku 5.5 (claude-haiku-5-5) · Skills run: /sdd:spec-analyze account-auth · Result: PARTIAL

## Summary

- Steps 1–4 ran for three rounds. Every finding got a decision. No AskUserQuestion call was made (scripted).
- Round 1 found all seven answer-key items (K1–K7). Round 1 also had 11 non-key findings. 7 are valid, 3 are arguable control-area findings, 1 is a false positive (F21).
- Apply step caused new defects. Round 2 found 3 conflicts that our own round-1 edits created. Round 3 found 4 more.
- Loop did not converge. Round 3 still had 13 open non-deferred findings. Round 3 was the cap, so its edits were applied and not re-checked.
- Plugin issues: analyst gets only a file path (no Open Questions). It re-raises deferred items. Options are not always exact text. Applied criteria break EARS. The skill has no merge rule and no rule for what happens at the round cap.

## Step trace

| Skill | Step | Action taken | Done-when held | Evidence |
|---|---|---|---|---|
| spec-analyze | 1 Load | Read requirements.md and .spec.json (Bash cat first, then Read) | Yes | `workspace/docs/specs/account-auth/requirements.md` (82 lines), `.spec.json` |
| spec-analyze | 2 Analyze | Dispatched spec-analyst (general-purpose, tools Read/Glob/Grep), input = file path only | Yes | Round 1 returned 21 findings (F1–F21) |
| spec-analyze | 3 Resolve | Walked high → medium → low. Scripted: high/med → A, low → Defer. Grouped by severity, 4 per call (see Q&A) | Yes | 21 decisions: 19 A, 2 Defer |
| spec-analyze | 4 Apply | Edited requirements.md per option. Deferred items → `## Open Questions`. Set design + tasks to `stale` | Yes, with defects (see Artifact checks) | `.spec.json` after: design `stale`, tasks `stale` |
| spec-analyze | 5 Recheck (round 2) | Dispatched spec-analyst again on edited file | Yes | 17 findings (F1–F17) |
| spec-analyze | 3–4 (round 2) | 12 A applied. 5 Defer (2 of them UNSCRIPTED: F13, F14 re-raise deferred items) | Yes | Decisions: 12 A, 5 Defer |
| spec-analyze | 5 Recheck (round 3, last) | Dispatched spec-analyst on file. Background run (a7d4…) used. Foreground re-run (a5c8…) also made by mistake, not applied | Yes | 15 findings (F1–F15) from a7d4 |
| spec-analyze | 3–4 (round 3) | 13 A applied, 2 Defer. Cap reached, no further recheck | Partial. Loop exit not met (13 open non-deferred items after apply) | Decisions: 13 A, 2 Defer |

## Scripted Q&A

Harness rule: no AskUserQuestion call. Each group below is the question the skill would ask. Answers come from the script.

| # | Question (as the skill would ask) | Options | Answer | Scripted? |
|---|---|---|---|---|
| R1-a | Round 1, F1–F4 (INCONSISTENCY pw length; INCONSISTENCY 2.1/2.4; INCONSISTENCY 4.1/4.2; CONFLICT 2.3/7.2) | A / B / Defer | A, A, A, A | Yes (high) |
| R1-b | Round 1, F5, F8, F9, F12 (FAILURE lock vs sessions; ASSUMPTION Tenant; EDGE support other tenant; EDGE reset link no expiry) | A / B / Defer | A, A, A, A | Yes (high) |
| R1-c | Round 1, F6, F7, F10, F13 (AMBIGUITY quickly; AMBIGUITY strong pw; ASSUMPTION Role/actor; FAILURE reset success only) | A / B / Defer | A, A, A, A | Yes (med) |
| R1-d | Round 1, F14, F15, F16, F17 (EDGE unknown email; EDGE duplicate sign-up; FAILURE mailer; FAILURE pw length error) | A / B / Defer | A, A, A, A | Yes (med) |
| R1-e | Round 1, F18, F19, F20 (EDGE 2.3 window; EDGE actor id for lock; FAILURE atomicity) | A / B / Defer | A, A, A | Yes (med) |
| R1-f | Round 1, F11, F21 (ASSUMPTION idle; EDGE creation old status) | A / B / Defer | Defer, Defer | Yes (low) |
| R2-a | Round 2, F1–F4 (INCONSISTENCY pw 3.3; INCONSISTENCY 4.1 vs revoke; CONFLICT 7.2/7.4; INCONSISTENCY Tenant on create) | A / B / Defer | A, A, A, A | Yes (high/med) |
| R2-b | Round 2, F5–F8 (AMBIGUITY case; FAILURE wrong pw response; EDGE unlock count; EDGE unlock unauth) | A / B / Defer | A, A, A, A | Yes (med) |
| R2-c | Round 2, F9–F12 (EDGE concurrent sign-up; EDGE multiple reset links; EDGE reset on locked; FAILURE reset pw error) | A / B / Defer | A, A, A, A | Yes (med) |
| R2-d | Round 2, F13, F14 (AMBIGUITY idle; FAILURE creation audit). Both re-raise deferred items | A / B / Defer | Defer, Defer | No. No script line for re-raised deferred items. Chose Defer (conservative). UNSCRIPTED |
| R2-e | Round 2, F15, F16, F17 (low: Argon2id cost; log fields; glossary terms) | A / B / Defer | Defer, Defer, Defer | Yes (low) |
| R3-a | Round 3, F1–F4 (INCONSISTENCY 3.1/3.3; INCONSISTENCY 1.5/3.3/5.9; INCONSISTENCY 2.4/2.5; CONFLICT 2.2/3.2) | A / B / Defer | A, A, A, A | Yes (high/med) |
| R3-b | Round 3, F5–F9 (EDGE check order; ASSUMPTION glossary; AMBIGUITY normalized email; AMBIGUITY idle; EDGE absolute lifetime) | A / B / Defer | A, A, A, A, A | Yes (med). F8 re-raises a deferred item |
| R3-c | Round 3, F10 (AMBIGUITY low: count reset) | A / B / Defer | Defer | Yes (low) |
| R3-d | Round 3, F11–F14 (INCONSISTENCY unlock order; AMBIGUITY creation audit; FAILURE queue; FAILURE record failure). F12 and F14 re-raise deferred items | A / B / Defer | A, A, A, A | Yes (med). F12, F14 re-raise deferred items |
| R3-e | Round 3, F15 (AMBIGUITY low: letter and digit) | A / B / Defer | Defer | Yes (low) |

Total: 53 questions. Would be 15 AskUserQuestion calls (6 + 5 + 4) in the real flow.

## Artifact checks

Artifact: `docs/specs/account-auth/requirements.md`

| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | Every finding resolved or deferred (step 3) | Pass | 53 decisions across 3 rounds |
| requirements.md | Deferred items under `## Open Questions` (step 4) | Pass | Lines 116–120. 3 items left after round 3 (F10, F15 round 3; Argon2id placeholders) |
| requirements.md | Option A gives exact criterion text (plugin rule) | Fail | See Issues 05-3. Round 1 F12 used `...`. Round 1 F16 had no target. Round 3 F4 left `[m]`, `[t]`, `[p]`, `[deployed capacity]` |
| requirements.md | Criteria are correct EARS (`shared/ears.md`) | Fail | One behavior per criterion broken: 2.3 (lock + revoke + reset count), 4.2 (3 sentences), 5.2 (replace + mark + revoke), 5.9, 1.6, 5.5, 7.2, 7.4 ("applied and queued"), 1.8. 7.3 and 5.8 have no `THE <System>` subject |
| requirements.md | Final state has no open non-deferred finding (step 5) | Not verified | Round 3 cap reached. Round 3 edits not re-checked. Round 3 a7d4 listed 13 open non-deferred items before apply |
| requirements.md | Edits did not conflict with other edits | Fail | Round 2 F3 (7.2 vs 7.4 lock exception vs one transaction). Round 3 F1 (3.1 vs 3.3 vs 1.1). Round 3 F13 (queue exception still violates 7.1 and 7.4) |
| .spec.json | Later phases `stale` after approved artifact edit (`shared/state.md:18`) | Pass | After: `"requirements": "approved", "design": "stale", "tasks": "stale"` |

### `.spec.json` before / after

Before:
```json
{
  "name": "account-auth",
  "workflow": "requirements-first",
  "order": ["requirements", "design", "tasks"],
  "phases": { "requirements": "approved", "design": "approved", "tasks": "approved" }
}
```

After:
```json
{
  "name": "account-auth",
  "workflow": "requirements-first",
  "order": ["requirements", "design", "tasks"],
  "phases": { "requirements": "approved", "design": "stale", "tasks": "stale" }
}
```

Snapshot of original workspace: `snapshots/round0/`.

## Answer-key scoring

Answer key (copied from brief, not passed to the analyst):
- K1 INCONSISTENCY: 1.1 password 8–64 chars vs 3.1 6–64 chars.
- K2 AMBIGUITY: 2.2 "quickly".
- K3 CONFLICT: 4.1 Sessions never expire vs 4.2 revoke after 30 min idle.
- K4 ASSUMPTION: "Tenant" (6.1) and "support agent"/`support` role absent from Glossary.
- K5 EDGE: sign-up with an email that already exists is unspecified.
- K6 FAILURE: Mailer down for 1.3 (welcome) and 5.1 (reset) unspecified.
- K7 EDGE: reset for an unknown email (5.1), and expired or used reset link (5.2), unspecified.
- Control: Requirement 7 is clean. Findings on it are false positives unless the argument is strong.

### Recall, round 1

| K | Found? | Round-1 finding | Note |
|---|---|---|---|
| K1 | Full | F1 | Correct citation 1.1 vs 3.1 |
| K2 | Full | F6 | |
| K3 | Full | F3 | Labeled INCONSISTENCY, not CONFLICT. Type mismatch only |
| K4 | Full | F8 (Tenant), F10 (`support` Role, caller, actor) | "support agent" term not named as such |
| K5 | Full | F15 | |
| K6 | Full | F16 | Covers 1.3 and 5.1 |
| K7 | Full | F14 (unknown email), F12 (no expiry), F13 (invalid/expired/used) | |

Rounds 2 and 3 found no new K item. They found follow-ups on the same areas (see below).

### Precision and control, round 1

Round 1 had 21 findings. 10 match K items. 11 are non-key:
- Valid, non-key (7): F2 (2.1 vs 2.4 correct password on locked), F5 (lock does not revoke sessions), F7 (strong passwords not measurable), F9 (support agent other tenant, no auth), F11 (idle undefined, low), F17 (no error for password length), F18 (2.3 window undefined).
- Control-area, arguable (3): F4 (2.3 vs 7.2 in audit outage; strong argument, contradiction is real), F19 (actor id for system lock; moderate), F20 (status write and audit not atomic; moderate).
- False positive (1): F21 (creation is not a status change under 7.1).

Round 2 (17 findings): 2 re-raise deferred items (F13 idle, F14 creation). 15 new. Judged valid. 3 were introduced by our round-1 edits (F1, F2, F3). Round 3 (15 findings, a7d4): 3 re-raise deferred items (F8 idle, F12 creation, F14 delivery log). 1 low item (F15) is valid but minor.

### Severity

- Round 1: sensible for most. F20 could be high (data integrity). F16 could be high (core flows).
- Round 2: F1, F2, F3 high is sensible. F13 and F14 re-raise deferred items; severity does not matter for them.
- Round 3: F1 high is sensible. Queue gap (a7d4 F13) is medium. Lock-without-audit risk is at least high. Medium is too low.

### Format (`agents/spec-analyst.md:22–31`)

- All 3 rounds matched the block keys (ID, TYPE, SEVERITY, AFFECTS, ISSUE, OPTIONS with A/B).
- Option A not always exact text:
  - R1 F12: `...` ellipsis.
  - R1 F16: no target criterion number.
  - R1 F3 B, F6 B, F7 B: `[N]`, `[source]` placeholders.
  - R3 F4 A: `[m]`, `[t]`, `[p]`, `[deployed capacity]` placeholders.
  - R2 F4 A and R3 F5 A are exact, but R3 F5 A names a `invalid_tenant` code that no criterion defined.

### Apply step

- Two round-1 A options on the same criterion conflicted: F4 A (lock applied on audit failure) and F20 A (one transaction, roll back). Round 2 F3 found it.
- Two round-1 A options edited 2.3: F5 A (revoke sessions) and F18 A (rolling window). Merged by hand. Skill has no merge rule.
- EARS not checked. Options produce multi-behavior criteria (see Artifact checks).
- Deferred items placed under `## Open Questions`. Pass.

### Recheck loop

- Rounds: 3 (max). Round 3 is the cap.
- Round 2 found new issues caused by our edits: F1, F2, F3 (and parts of F5). Round 3 found new issues caused by round-2 edits: F1, F2, F11, F13.
- After round 3, 13 non-deferred findings remained open. The skill exit condition ("no open non-deferred finding") was not met.

### AskUserQuestion count

- Real flow: 53 questions in 15 calls (round 1: 21 → 6 calls; round 2: 17 → 5 calls; round 3: 15 → 4 calls). Rule: ≤4 per call.
- Grouping was by severity because the skill does not define "group related".

## Issues

| ID | Severity (high/med/low) | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| 05-1 | high | `skills/spec-analyze/SKILL.md:15`; `agents/spec-analyst.md:7` | Analyst gets only the file path. It does not see `## Open Questions` or `.spec.json`. It re-raised 5 deferred items (R2 F13, F14; R3 F8, F12, F14). | Pass the Open Questions list and state to the analyst. Tell it to skip items already deferred. |
| 05-2 | high | `skills/spec-analyze/SKILL.md:19–20`; `shared/ears.md:23–24` | Apply step does not check EARS. Options produce multi-behavior criteria and subject-less criteria (2.3, 4.2, 5.2, 5.9, 7.2, 7.3, 7.4, 1.6, 5.5, 5.8). | Step 4: after applying, check each new criterion against `shared/ears.md` (one behavior, `THE <System>` subject). Split or reject violators. |
| 05-3 | high | `agents/spec-analyst.md:22–31`; `skills/spec-analyze/SKILL.md:17` | Option A is not always exact criterion text: `...`, `[N]`, `[m]`, "Add:" with no target. Apply step cannot apply it verbatim. | Require full replacement criterion text with target number. No placeholders. If the owner must choose a number, return `NEEDS_OWNER` instead of option A. |
| 05-4 | high | `skills/spec-analyze/SKILL.md:19–21` | Applied edits conflicted with each other (R2 F3, R3 F1, R3 F13). No rule to detect or merge two options that change the same criterion. | Step 4: if two chosen options edit the same criterion, merge them and show the merged text. Step 5: analyst must read the whole applied document (it already does), so keep recheck mandatory. |
| 05-5 | medium | `skills/spec-analyze/SKILL.md:21` | "Max 3 rounds" does not say what happens to round-3 edits. Round 3 edits were applied with no recheck. The skill has no exit path for unresolved findings. | Define the cap. After round 3, list open non-deferred findings in the report and stop. Do not apply unverified edits, or allow a verify-only round. |
| 05-6 | medium | `skills/spec-analyze/SKILL.md:17` | "group related" is not defined. Grouping by severity gives 15 calls for 53 questions. | Define a grouping rule (for example, same AFFECTS requirement). Keep ≤4 per call. |
| 05-7 | medium | `skills/spec-analyze/SKILL.md:17` | No rule for a finding that duplicates an earlier deferred item or an earlier applied fix. | Add: a finding that repeats a deferred item or a resolved item is marked as a duplicate and not asked again. |
| 05-8 | medium | `skills/spec-analyze/SKILL.md:6` | `allowed-tools` lists `Task`. Subagent dispatch in the current runtime uses `Agent`. Bash and Write are not listed. Reads used Bash in step 1. | Align the tool name with the runtime (`Agent`). Document which tool reads the file. |
| 05-9 | medium | `agents/spec-analyst.md:33` | Analyst reported a false positive (F21: creation is not a status change under 7.1). It also reported control-area items with moderate arguments (F19, F20). No control rule. | Tell the analyst to check each finding against the text of the criterion it cites. Add a rule: findings must quote the criterion text they dispute. |
| 05-10 | low | `agents/spec-analyst.md:18` | Done-when says "every requirement pair sharing a term" but does not say which terms. Analyst still missed `support agent` as a term (K4 partial). | Add a term list: every capitalized or backticked term in the Glossary and in the criteria. Check each one against the Glossary. |

## Ambiguity log

- "Ask via AskUserQuestion (group related, ≤4 per call)" → grouped by severity, 4 per call → "related" not defined.
- "Option A | option B | Defer" → when option A had placeholders (`[N]`), applied the placeholder text as written → no rule for unfilled values.
- "Edit artifact per chosen options" → option text said "Add to Requirement X" with no criterion number → new criterion appended at the end of the requirement → no placement rule.
- "Repeat steps 3–4 until NO FINDINGS or only deferred remain. Max 3 rounds." → round 2 re-raised deferred items. Treated as UNSCRIPTED, Defer (conservative).
- "Max 3 rounds" → round 3 was applied and not re-checked → read as: round 3 is the last dispatch; its findings are resolved and applied, not verified.
- Option A text for two findings on the same criterion (R1 F5, R1 F18 on 2.3) → merged into one criterion → no merge rule.
- Option A text for R1 F4 (7.2 lock exception) and R1 F20 (7.4 one transaction) → applied both → produced a conflict (R2 F3).
- `allowed-tools: ... Task` → used `Agent` (the runtime's subagent tool) → name mismatch.
- Step 1 "read requirements.md + .spec.json" → used Bash `cat` first (Bash not in allowed-tools), then Read → harness log issue, not a plugin defect.

## Metrics

- Questions asked: 53 (would be 15 AskUserQuestion calls). Actual AskUserQuestion calls: 0 (scripted).
- Subagent dispatches: 4 (spec-analyst: round 1 ×1, round 2 ×1, round 3 ×2 — one was a duplicate foreground re-run, a5c8…, whose findings were not applied).
- Gates: 0 (spec-analyze has no gate step).
- Tests run: 0 pass / 0 fail (workspace has no tests; no Python run).

REPORT: /Users/baodang/Documents/code/agent-skills/docs/sdd-eval/05-analyze-haiku/report.md RESULT: PARTIAL ISSUES: 10
