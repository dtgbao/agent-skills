# 04-designfirst-haiku

Model: Haiku 5.5 · Skills run: spec-new (Design-First) · Result: PARTIAL

## Summary

- The Design-First flow ran to the end. Gates 1 to 3 passed with scripted answers. spec-run was not run.
- The late answer ("export one note by id", "write to a file") had no rule to apply. I kept design.md unchanged. I listed both needs under a Gaps section in requirements.md.
- Step 7 edits an approved design. Under `shared/state.md:18`, requirements (just approved) becomes `stale`. No step re-gates requirements. The spec ends with requirements `stale`.
- design.md cites only 3 of 8 requirement criteria. No step checks this link.
- tasks.md graph validator: PASS (8 checks). Wave dependency rule cannot be checked from the file.
- Process deviation: I wrote the two Gaps items before the step 6 question was asked. The answer text matches. Logged, not hidden.

## Step trace

| Skill | Step | Action taken | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1 Name | Name `notes-export-subcommand` | Yes | `workspace/docs/specs/notes-export-subcommand/` |
| spec-new | 2 Size | Spec needed, not a typo | Yes | Input is a feature |
| spec-new | 3 Workflow | Input names Design-First, used it | Yes | Input text |
| spec-new | 4 State | Created `.spec.json`, order design→requirements→tasks | Yes | `evidence/after-step4-state.json` |
| design-first | 1 Level | Asked. Answer Low-Level | Yes | Q1 |
| design-first | 2 Context | Read README.md (fixed architecture), notes/cli.py, repo.py, model.py, tests | Yes | README.md:6-11 |
| design-first | 3 Draft design.md | Drafted Low-Level design. Properties empty | Yes (see Artifact checks) | `evidence/design-gate1.md` |
| design-first | 4 Gate 1 | Count line: 3 components, 1 Mermaid, 1 file tree diff, 2 call tree diffs. Approve | Yes | `evidence/after-gate1-state.json` |
| design-first | 5 Requirements | Drafted requirements.md: 2 requirements, 8 criteria, Gaps section | Partly (see 04-5) | `evidence/requirements-gate2.md` |
| design-first | 6 Gate 2 | Asked "Which user needs…". Answer recorded in Gaps. Approve | Yes | Q3, Q4, `evidence/after-gate2-state.json` |
| design-first | 7 Properties | Added Property 1 (markdown, invariant) and Property 2 (json, round-trip). Edited approved design. Set requirements and tasks to `stale`. Drafted tasks.md | Yes | `evidence/design-after-step7-props.md`, `evidence/after-step7-state.json` |
| design-first | 8 Gate 3 | Count line: 8 leaves, 3 groups, 2 checkpoints, 5 waves. Approve. Set tasks `approved` | Yes | `evidence/after-gate3-state.json` |
| design-first | 8 Next step | Would tell user `/spec-run notes-export-subcommand`. Not run | n/a | — |

## Scripted Q&A

| # | Question (as the skill would ask) | Options | Answer | Scripted? |
|---|---|---|---|---|
| Q1 | Level? (design-first.md:7) | High-Level (architecture, flows, NFRs) \| Low-Level (interfaces, algorithms, pseudocode) | Low-Level | Yes |
| Q2 | Design gate: design.md drafted, count line. (gate.md:5-6) | Approve \| Request changes | Approve | Yes |
| Q3 | Which user needs does this architecture miss? (design-first.md:15) | Free text. No options given | Users need to export one note by id (`--id N`) and to write to a file path (`--out PATH`) instead of stdout. | Yes |
| Q4 | Requirements gate: 8 criteria. (gate.md:6) | Approve \| Request changes \| Analyze first | Approve | Yes |
| Q5 | Tasks gate: 8 leaves, 5 waves. (gate.md:6) | Approve \| Request changes | Approve | Yes |

No AskUserQuestion call was made. All answers came from the script.

## Artifact checks

### design.md (Done-when, shared/artifacts/design.md)

| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| design.md | every criterion maps to ≥1 component (line 4) | Pass at gate 1 (3 provisional criteria). **Fail** against final requirements: 1.3, 1.4, 1.5, 2.2, 2.3 have no `_Requirements_` cite | design.md `_Requirements: 1.1, 1.2_`, `_Requirements: 2.1_` |
| design.md | every external dependency has Error Handling entry (no line; implied) | Pass | Error Handling: notes.json missing, invalid JSON, stdout failure |
| design.md | every component has interface sketch (line 6) | Pass after fix. First draft had no NoteRepo sketch. Added before gate 1 | design.md NoteRepo block |
| design.md | ≥1 Mermaid diagram (implied) | Pass | flowchart LR |
| design.md | File/Folder Structure shows file tree as diff (line 8) | Pass | `diff` block, new export.py and test files marked `+` |
| design.md | every changed component has component/call tree as diff (line 9) | Pass. cli.py call tree diff. export.py whole-block call tree diff. repo.py and model.py unchanged, no view | design.md Components section |
| design.md | Testing Strategy lists every property (line 10) | Pass after step 7 (Property 1, 2 listed). At step 3 it passed only because the list was empty | design.md Testing Strategy |
| design.md | every NFR has owner (line 11) | Pass (vacuous). No NFR in the request | — |

### requirements.md (Done-when, shared/artifacts/requirements.md)

| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | every requirement has ≥1 criterion, numbered N.M | Pass | Req 1 (1.1–1.5), Req 2 (2.1–2.3) |
| requirements.md | one EARS pattern, one behavior, one observable | Pass after two self-edits. 1.5 and 2.3 had a second observable (stderr message, "print no export"). Removed | requirements.md 1.5, 2.3 |
| requirements.md | every system/actor term in Glossary | Pass | Notes CLI, Note, Exporter, Export |
| requirements.md | every input has bound or format | Pass | `--format` enum; id integer |
| requirements.md | every happy-path criterion has failure/edge criterion | Pass | 1.1→1.3; 1.2→1.3; 1.1/1.2→1.4; 2.1→2.3 |
| requirements.md | zero unmeasured adjectives | Pass | — |
| design-first step 5 | every component has ≥1 criterion | Pass | Exporter (1.1–1.3), CLI (2.1–2.3), NoteRepo (1.4, 1.5), Note (1.1, 1.2) |

### design.md properties (shared/correctness.md)

| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| design.md | every criterion classified | Pass | 8 criteria classified (design.md Classification list) |
| design.md | every property validates ≥1 criterion | Pass | Property 1 → 1.1. Property 2 → 1.2 |
| tasks.md | every property has task | Pass | Leaves 2.3 (Property 1), 2.4 (Property 2) |

### tasks.md (Done-when, shared/artifacts/tasks.md)

| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| tasks.md | every criterion cited by ≥1 leaf | Pass | Validator: criteria=8, uncited=[] |
| tasks.md | every leaf in exactly one wave | Pass | Validator |
| tasks.md | every leaf names its files | Pass | Validator |
| tasks.md | graph JSON parses | Pass | Validator |
| tasks.md | wave rule: leaf strictly after dependency waves | **Cannot check**. Graph JSON has no dependency field | tasks.md:17 |
| tasks.md | wave rule: same-wave leaves disjoint files | Pass | Validator |

### Validator output (`validate_graph.py`, saved in scenario dir)

```
[PASS] graph JSON parses
[PASS] every leaf in exactly one wave -- dup=[] missing=[] extra=[]
[PASS] wave ids start at 0 and are contiguous -- [0, 1, 2, 3, 4]
[PASS] same-wave leaves touch disjoint files -- []
[PASS] every leaf names its files -- []
[PASS] every criterion cited by >=1 leaf -- criteria=8 uncited=[]
[PASS] property leaves carry Validates line -- props=['2.3', '2.4'] bad=[]
[PASS] checkpoints not in graph

Wave table:
  wave 0: 1.1
  wave 1: 2.1
  wave 2: 2.2, 2.3, 4.1
  wave 3: 2.4, 4.2
  wave 4: 4.3

RESULT: PASS
```

## Extra checks

### A. Late answer after design approval

- Did any step say update design.md? **No.** design-first.md:15 gives the question. It gives no rule for the answer. gate.md:7 says "edit artifact" but does not name which.
- Did the stale rule fire at gate 2? **No.** No approved artifact was edited between gate 1 and gate 2. requirements.md was still a draft.
- What I did: needs went to requirements.md Gaps, not into criteria. Basis: design-first.md:13 ("Scope = what design supports"). design.md was not edited.

`.spec.json` after gate 2:
```json
{"name": "notes-export-subcommand", "workflow": "design-first", "order": ["design", "requirements", "tasks"], "phases": {"requirements": "approved", "design": "approved", "tasks": "pending"}}
```

### B. Step 7 edit to approved design

- Does the edit make later phases stale? **Yes.** state.md:18: "Edit approved artifact → every later phase in `order` becomes `stale`." Design was approved. Edit adds properties at step 7. Later phases: requirements (approved at gate 2) and tasks.
- What I did: followed step 7 literally. Set requirements and tasks to `stale`. Then drafted tasks.md and approved it at gate 3. gate.md:8 sets `approved` and does not mention `stale`.
- Result: requirements stays `stale`. Nothing in this flow re-gates requirements. Only `/spec-sync` clears `stale` (state.md:18), and that is outside this brief.

`.spec.json` after step 7 (stale applied):
```json
{"name": "notes-export-subcommand", "workflow": "design-first", "order": ["design", "requirements", "tasks"], "phases": {"requirements": "stale", "design": "approved", "tasks": "stale"}}
```

`.spec.json` after gate 3 (final):
```json
{"name": "notes-export-subcommand", "workflow": "design-first", "order": ["design", "requirements", "tasks"], "phases": {"requirements": "stale", "design": "approved", "tasks": "approved"}}
```

`.spec.json` after gate 1 and after step 4 (for reference):
```json
{"name": "notes-export-subcommand", "workflow": "design-first", "order": ["design", "requirements", "tasks"], "phases": {"requirements": "pending", "design": "approved", "tasks": "pending"}}
```
(step 4 state: all `pending`)

### C. Design views (shared/visuals.md)

- File tree diff: used. design.md File/Folder Structure.
- Call tree diff for cli.py `main`: used. Shows added `export` subparser and branch.
- Call tree for new export.py: used as whole block (visuals.md:3, "show a whole block when most of it is new").
- Component tree: not used. No UI.
- Unclear: whether a new file needs a view at all (see 04-10).

## Issues

| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| 04-1 | high | shared/workflows/design-first.md:15 | Gate 2 question has no rule for applying a "missing needs" answer. Target artifact not named (design or requirements). | Add rule: needs the design misses → record as Gaps, or Request changes on design with stale cascade. Name which. |
| 04-2 | high | shared/workflows/design-first.md:16; shared/state.md:18 | Step 7 edits approved design. Stale rule sets approved requirements to `stale`. No step re-gates requirements. Only `/spec-sync` clears it, and this flow never calls it. | Move property authoring before the design gate, or add a re-approve step for requirements after step 7. |
| 04-3 | med | shared/workflows/design-first.md:10 | Says "Properties list stays empty until step 5". Properties are added at step 7 (line 16). Step 5 is requirements. | Change to "until step 7". |
| 04-4 | med | shared/artifacts/design.md:4 | "every criterion maps to ≥1 component" runs before requirements exists. Criteria source is not defined. | Define criteria list in design step 2 (from request or constraints), or move the check to after requirements. |
| 04-5 | med | shared/workflows/design-first.md:14 | Requirements Done-when checks only "every component has ≥1 criterion". No reverse check. design.md cites 3 of 8 requirement criteria. | Add reverse check: every requirement criterion cites ≥1 design component. Or re-open design gate. |
| 04-6 | med | shared/gate.md:6 | "Requirements phase adds: Analyze first". Unclear whether design-first's requirements gate (step 6) is "requirements phase". I did not offer it. | Name the workflows where Analyze first applies. |
| 04-7 | med | shared/gate.md:8; shared/state.md:18 | Approve sets `approved` but does not clear `stale`. Tasks was `stale` before gate 3. Gate 3 set `approved`. Behavior undefined. | State that Approve sets `approved` and clears `stale`. |
| 04-8 | med | shared/artifacts/tasks.md:17 | Wave rule "strictly after every wave holding its dependencies" needs a dependency list. Graph JSON has none. Rule cannot be checked. | Add `deps` per leaf to the graph JSON. Or drop the rule. |
| 04-9 | low | shared/artifacts/tasks.md:11 | "One after each layer" — "layer" not defined. | Define layer = top-level group. |
| 04-10 | low | shared/artifacts/design.md:9; shared/visuals.md:3 | "every changed component" — unclear for a new file. I used a whole-block call tree. | State: new component → whole-block diff of its call tree. |
| 04-11 | low | shared/artifacts/design.md:6 | "every component has interface sketch" — unclear for unchanged components (NoteRepo). First draft lacked it. | Scope to new and changed components. Or state that unchanged ones are listed by signature. |
| 04-12 | low | skills/spec-new/SKILL.md:13 | "Kebab-case from input" — no length or word rule. Input is one long sentence. | Add max length and word-selection rule. |

## Ambiguity log

- "Which user needs does this architecture miss?" → recorded in requirements.md Gaps, no design edit → design-first.md:13 (scope = design); state.md:18 would cascade. No rule covers the answer.
- Name → `notes-export-subcommand` → spec-new/SKILL.md:13 has no length rule.
- Properties step → added at step 7 → design-first.md:16 (line 10 says step 5).
- Stale on pending tasks → set `stale` literally → state.md:18 says "every later phase".
- Stale on tasks after approve → set `approved` at gate 3 → gate.md:8 does not mention stale.
- EXPORTERS location → `notes/export.py` → README.md:11 does not name a file.
- Default export format → `markdown` → my choice. Not in request.
- Design criteria IDs → provisional 1.1, 1.2, 2.1 → requirements later had 8 criteria. Numbers coincide only for those three.
- Edits made before gate 2 for EARS rule: removed second observables in 1.5 and 2.3 → ears.md:23.

## Hard-to-follow instructions (small-model view)

1. design-first.md:10 — "Properties list stays empty until step 5." Step 5 is requirements. Properties come at step 7 (line 16).
2. design-first.md:16 — "Add properties to `design.md`..." after design approval. Conflicts with state.md:18 (stale cascade). No recovery step.
3. design-first.md:15 — "Gate. Prompt user: 'Which user needs does this architecture miss?'" No rule to apply the answer.
4. design.md:4 (shared/artifacts/design.md) — "every criterion maps to ≥1 component or property (cite `_Requirements: x.y_` on component)". Criteria source not defined at draft time.
5. gate.md:6 — "Requirements phase adds: Analyze first (runs `/spec-analyze` flow)." Unclear whether design-first requirements gate qualifies.
6. gate.md:8 — "Approve → set phase `approved`". Silent on `stale`.
7. tasks.md:17 — "strictly after every wave holding its dependencies." No dependency field in graph.
8. tasks.md:11 — "One after each layer, one final." "Layer" undefined.
9. visuals.md:3 and design.md:9 — "Show a whole block when most of it is new" vs. "every changed component shows ... as a diff block." New file ambiguous.
10. design.md:6 — "every component has interface sketch." Unchanged components ambiguous.
11. spec-new/SKILL.md:13 — "Kebab-case from input." No length rule.
12. design.md:11 — "every non-functional constraint ... has an owner component." Vacuous here. Not checkable with no NFRs.

## Metrics

- Questions asked: 5 (all scripted, 0 UNSCRIPTED) · Subagent dispatches: 0 · Gates: 3 · Tests run: pytest 0 (no code phase; not run) · Validator: 8 pass / 0 fail

## Files

- `workspace/docs/specs/notes-export-subcommand/` — spec output (design.md, requirements.md, tasks.md, .spec.json)
- `validate_graph.py` — tasks.md graph checker
- `evidence/` — state and artifact snapshots per gate
- Plugin files not edited. No commits. No branch change.
