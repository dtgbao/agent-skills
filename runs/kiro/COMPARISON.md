# Kiro vs sdd: artifact comparison

Kiro samples: `rate-limit` (NestJS), `clerk-authentication` (Next.js), `airbnb-clone` (Next.js + Convex). Source: `~/Downloads/kiro-specs/`.
sdd samples: specs that the eval sessions made (01, 02, 03, 04, 06). Raw numbers: [metrics.md](metrics.md), script: [measure.py](measure.py).

Caveat: the inputs differ. The Kiro specs target real repos with a framework. The sdd specs target small Python fixtures. Compare shape and ratios, not totals. `kiro/rate-limit` vs `sdd/01`, `sdd/02` is the closest pair.

## Verdict

sdd copies the Kiro skeleton well: the same headings, EARS, the Glossary, `*For any*` properties with `**Validates:**`, `*` optional leaves, checkpoints, and the wave graph JSON. sdd is stricter than Kiro on traceability, and that is good.

sdd differs from Kiro in two ways that matter:

1. **Requirements are fewer and longer.** Kiro splits a feature into 6–9 small capability requirements with short criteria. sdd made 1–3 requirements with long, compound criteria. The analyze loop is the main cause.
2. **Task leaves are thin.** A Kiro leaf is a small work order: the file, the steps, the test cases, the command. An sdd leaf is a title plus `Files:` and `_Requirements:_`.

## Shape side by side

| Measure | Kiro rate-limit | Kiro clerk | Kiro airbnb | sdd 01 (Sonnet) | sdd 02 (Haiku) | sdd 06 (Quick) |
|---|---|---|---|---|---|---|
| Requirements | 6 | 8 | 9 | 3 | **1** | 2 |
| Criteria | 20 | 45 | 79 | 17 | 8 | 13 |
| Criteria per requirement | 3.3 | 5.6 | 8.8 | 5.7 | **8** | 6.5 |
| Words per criterion (mean / max) | 21 / 27 | 22 / 44 | 34 / 80 | 35 / 86 | **42 / 99** | 17 / 28 |
| `IF` (unwanted) criteria | 0 % | 29 % | 23 % | 18 % | 25 % | 23 % |
| Design properties | 6 | 3 | 18 | 9 | 5 | 5 |
| Design code blocks (real code) | 6 | 10 | 9 | 2 | 1 | 2 |
| Design `diff` views | 0 | 0 | 0 | 3 | 4 | 3 |
| `_Requirements:_` on design components | 0 | 0 | 0 | 3 | 2 | 2 |
| Task leaves | 13 | 19 | 57 | 6 | 10 | 8 |
| Words per leaf | 61 | 49 | 46 | 35 | 22 | 22 |
| Detail bullets per leaf | 4.3 | 3.8 | 3.6 | 2.7 | 2.5 | 2.6 |
| Leaves that name files | 2 / 13 | 19 / 19 | 35 / 57 | 6 / 6 | 10 / 10 | 8 / 8 |
| Criteria cited by a task | 18 / 20 | 40 / 45 | 76 / 79 | 17 / 17 | 8 / 8 | 13 / 13 |
| Widest wave | 5 | 5 | 15 | 2 | 3 | 4 |

## Where sdd matches Kiro

| Element | Kiro | sdd |
|---|---|---|
| Requirements headings | Introduction, Glossary, Requirements, User Story, Acceptance Criteria | same |
| Glossary terms | `Snake_Case` names (`Rate_Limiter`, `Time_Window`), used as EARS subjects | free form (`Shortlinks API`); add the Kiro rule to `ears.md` |
| Criterion numbering | `1.` per requirement, cited as `2.3` | same (the sdd Done-when text says `N.M`, which reads as a conflict, see 01-5) |
| Property form | `*For any* … SHALL …` + `**Validates: Requirements x.y**` | same |
| Property tag | `// Feature: <spec>, Property N: <title>`, ≥100 runs | same |
| Optional leaves | `- [ ]*`, Notes line "skip for faster MVP" | same |
| Property leaf | bold `**Property N: …**` + `**Validates:**` | same |
| Checkpoint | top-level task, "Ensure all tests pass, ask the user if questions arise." | same idea, shorter text |
| Graph | `## Task Dependency Graph`, `waves` JSON, leaves only | same |

## Where sdd is stricter than Kiro (keep)

| Rule | Kiro sample | sdd |
|---|---|---|
| Every criterion cited by ≥1 leaf | misses 2–5 criteria per spec (e.g. rate-limit 2.4 "window reset", 6.3 "guard order") | 100 % in every run |
| Leaf names its files | rate-limit: 2 of 13 | all leaves |
| Same-wave leaves touch disjoint files | rate-limit wave 3 has property leaves 2.2–2.5 with no files named; they likely share one test file | enforced |
| `_Requirements:_` on each design component | none (only properties carry `Validates`) | yes |
| Shape views (`diff` file tree, call tree) | none | yes |
| State file, gates, analyze, sync | not in the export | yes |

These rules make parallel wave runs safe. Kiro does not need them as much, because its runner is not parallel in the same way.

## Where sdd falls short of Kiro (change)

### 1. Requirement granularity

Kiro makes one requirement per user-visible capability. For rate limiting: config, enforce, per-route override, exempt, headers, guard order. Each has 3–4 short criteria.

sdd 02 made one requirement with 8 criteria. Criterion 1.8 has 99 words and five behaviors. The analyze loop appended each option A to the nearest criterion.

Proposed changes:
- `artifacts/requirements.md`: "One requirement = one capability that a user or operator can observe. 2–7 criteria each. One `SHALL` per criterion, ≤40 words."
- `spec-analyze` step 4: "An option that adds a behavior adds a new criterion or a new requirement. It never extends an existing criterion."

### 2. Strictness of the requirements Done-when

The Kiro rate-limit spec fails 3 of 6 sdd requirements checks: it has no failure criteria (0 `IF`), the env var inputs have no bounds, and "route handler" is not in the Glossary. Kiro still produced a usable spec. The sdd rule "every happy-path criterion has ≥1 failure or edge criterion" pushes the model to add one failure criterion per criterion. The analyze loop then adds more.

Proposed change: "every requirement has ≥1 failure or edge criterion when it takes input or calls a dependency". This matches Kiro clerk and airbnb (23–29 % `IF`), and sdd already lands in that range.

### 3. Leaf detail

A Kiro leaf has 3–4 sub-bullets: the exact command (`pnpm add …`), the function to export, the test cases to write, and the test file path. A runner subagent can act on it without the design. An sdd leaf often has one line of title, `Files:`, and `_Requirements:_`. The runner must read design.md to know what to build.

Proposed change to `artifacts/tasks.md` leaf format:

```markdown
  - [ ] 2.1 Create `src/proxy.ts` with `clerkMiddleware`
    - Files: `src/proxy.ts`
    - Do: <1–3 bullets: what to create, export or change>
    - Verify: <test cases or command that proves it>
    - _Requirements: 2.1, 2.2_
```

This keeps the sdd `Files:` field and adds the Kiro "Do" and "Verify" detail. It also fixes 06-7 (the runner did not know which tests to run).

### 4. Design code sketches

Kiro designs show real code for every component: the module registration, the decorator usage, the type of the return value (6–10 code blocks). sdd designs replace most of this with `diff` call trees (1–2 code blocks). Both are useful. Call trees show the flow. Code shows the contract.

Proposed change: Done-when "every new or changed component has an interface sketch in the project language (signature or type)". Keep `diff` views for structure only, and only where the shape changes (01 report: `_LogThrottle` had no useful call tree).

### 5. Component headings

Kiro clerk uses the file path as the component heading: `#### src/lib/clerk-env.ts — Environment Validation`. sdd uses `### <Component> (<path>)`. Both work. The Kiro form makes `Files:` in tasks trivial to fill. Optional change.

### 6. Several properties per test leaf

Kiro clerk leaf 2.3 holds Property 2 and Property 3 in one test file. sdd `correctness.md` says "task per property", so sdd 02 put 5 properties in 5 waves (02-8). Change: "one leaf per test file; a leaf may hold several properties".

### 7. Final checkpoint names the commands

Kiro final checkpoint: "Run `pnpm test --run` and `pnpm typecheck`." sdd checkpoints have no command, and `spec-run` must guess (06-5). Change: the tasks drafter writes the test and typecheck commands into the final checkpoint, read from the manifest or README.

## Things to check in Kiro output that the samples do not show

- No Bugfix or Design-First sample. The sdd bugfix and design-first skeletons cannot be compared.
- The exports name the file `task.md`. sdd uses `tasks.md`. Confirm the Kiro name before you change sdd.
- Kiro design section order varies (airbnb puts Correctness Properties after Testing Strategy; clerk nests all sections under one `##`). Kiro does not enforce a strict order. sdd should keep its fixed order. A fixed order is easier for skills and validators to check.
