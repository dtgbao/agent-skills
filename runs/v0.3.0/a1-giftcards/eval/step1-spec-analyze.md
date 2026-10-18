# Step 1: /sdd:spec-analyze gift-cards

Invocation: manual load (task came as plain text from the parent session).
Resolved path example: `/Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/scripts/spec.py`.
Agent type `sdd:spec-analyst` available. Agent reported Sonnet 5.5, tools Read, Glob, Grep (+SubagentHandback). Frontmatter applied.

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-analyze | 1 Load | `SPEC drift` → NO DRIFT; read requirements.md + .spec.json | yes | requirements approved, design/tasks pending |
| spec-analyze | 2 Analyze | D1 FULL, next id F1 | yes | 13 findings |
| spec-analyze | 3 Resolve | 10 high/medium → A (3 grouped calls); 3 low deferred | yes | QA.md calls 1–3 |
| spec-analyze | 4 Apply | edits + EARS splits; `SPEC edited` | yes | 4.2 deleted; 1.1→1.1+1.5; F5/F7 split |
| spec-analyze | 5 Recheck r2 | D2 FULL → 6 findings → A; `SPEC edited` | yes | F17/F19 split |
| spec-analyze | 5 Recheck r3 | D3 FULL → 4 findings (3 medium → A, 1 low deferred); `SPEC edited` | yes | F21 split (two SHALLs) |
| spec-analyze | 5 Verify | D4 VERIFY on 22 changed ids → 3 medium to Open Questions | yes | F24–F26 |

## Result
- Criteria 13 → 28. All changed criteria: one SHALL, ≤31 words.
- Open Questions: F11, F12, F13, F22 (low), F24, F25, F26 (medium, verify).
- `.spec.json`: requirements still `approved`, hash updated by `SPEC edited` (×4). Final drift: NO DRIFT.
- Questions: 19 (all scripted option A). NEEDS_OWNER chosen: 0. UNSCRIPTED: 0.

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| A1 | medium | agents/spec-analyst.md:28 | Options often hold two assertions or two SHALLs (F5, F7, F9, F17, F19, F21, F24). Orchestrator had to split 7 times. | Add "one observable assertion" and cite `shared/ears.md` rules in the agent. |
| A2 | low | agents/spec-analyst.md:29 | NEEDS_OWNER shows as option B with a stray `A)` label (F3, F6, F8, F11–F13). Rule says single option A. | Say: "NEEDS_OWNER only as the sole option; never as B." |
| A3 | medium | agents/spec-analyst.md:27 | Options A/B are sometimes complementary, not alternatives (F7, F9, F10). One pick drops a real fix. | Require A and B to be mutually exclusive; separate gaps → separate findings. |
| A4 | medium | skills/spec-analyze/SKILL.md:22 | Every FULL round found new medium items; 3-round cap ends with 3 medium items unresolved in Open Questions. Criteria doubled. | Accept by design, or give VERIFY findings one resolve pass for high only. |
| A5 | low | skills/spec-analyze/SKILL.md:19 | No rule for an option part already covered by another criterion (F18 "return 503" vs 5.2). | Add: "drop option parts that duplicate an existing criterion; log it." |
