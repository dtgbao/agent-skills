# Spec-Driven Development Workflow

A plugin for spec-driven development, with **four entry
workflows** routed through a single unified command:

| Workflow               | Best for                                                                                                             | Produces, in order                                                      |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Requirements-First** | Clear user-facing behavior, flexible technical approach, greenfield work                                             | requirements.md → design.md → tasks.md                                  |
| **Design-First**       | A known tech stack, strict non-functional requirements, an existing architecture/diagram, or feasibility exploration | design.md → requirements.md → tasks.md                                  |
| **Bugfix**             | Something already built is behaving incorrectly                                                                      | bugfix.md → design.md → tasks.md                                        |
| **Quick Spec**         | A small, well-understood feature where you trust the output                                                          | requirements.md, design.md, tasks.md — generated back-to-back, no gates |

Every phase's logic lives in a **skill** (`skills/<name>/SKILL.md`).
Each **command** (`commands/<name>.md`) is a thin pointer that just
tells Claude to read and follow the matching skill — commands exist purely
for discoverable, predictable `/name` invocation; all the actual instructions
live in one place.

## Start here: `/spec-new`

If you're not sure which workflow fits, run `/spec-new <what you want to
build or fix>`. It weighs your description against the table above,
recommends one workflow with a one-line reason, lists the other three so
you can override it, and — once you confirm — hands straight off to the
right skill with no need to re-type your description. Power users can
still jump straight to `/spec-requirements`, `/spec-design`,
`/spec-bugfix`, or `/spec-quick` and skip the picker entirely.

## Requirements-First and Design-First (feature specs)

Both produce the same three files and go through the same skills
(`spec-requirements`, `spec-design`, `spec-tasks`) — they just run in a
different order, and `spec-design` asks for a **detail level** (High Level
or Low Level) when it's the entry point instead of a continuation:

```
Requirements-First                        Design-First
───────────────────                       ────────────
/spec-requirements <name>                 /spec-design <description>
  → requirements.md    ── approve ──┐       → design.md         ── approve ──┐
                                    ▼                                        ▼
/spec-design <slug>                       /spec-requirements <slug>
  → design.md          ── approve ──┐       → requirements.md   ── approve ──┐
                                    ▼                                        ▼
/spec-tasks <slug>                        /spec-tasks <slug>
  → tasks.md           ── approve ──┐       → tasks.md          ── approve ──┐
                                    ▼                                        ▼
/spec-execute <slug> [n]  → implements one task, checks it off, repeat
/spec-status [slug]       → check progress any time
```

Each phase skill refuses to run ahead of what it needs (`spec-design` in
Requirements-First mode won't start without requirements.md; in
Design-First mode there's nothing to wait for since it _is_ the start), and
each phase ends by showing you the draft and waiting for "approved" before
the next phase is available.

The generated documents follow a consistent shape:

- **requirements.md** opens with a **Glossary** defining the system and its
  key nouns (`Application`, `Client`, `Protected_Route`, ...), so every
  acceptance criterion can say "THE `<Term>` SHALL ..." instead of a vague
  "the system." In Design-First, the glossary reuses component names
  design.md already established.
- **design.md** includes a **Correctness Properties** section when the
  feature has universal invariants worth property-based testing (e.g. rate
  limits, parsers, validators) — each property states a "for any X, Y must
  hold" guarantee and traces back to requirement numbers. In Design-First,
  you're asked to pick **High Level** (architecture-first, good for teams)
  or **Low Level** (pseudocode/interfaces-first, good for fast feasibility
  checks).
- **tasks.md** groups work into parent tasks with numbered subtasks
  (`1`, `1.1`, `1.2`, ...), marks optional work with `- [ ]*`, inserts
  **Checkpoint** tasks that run the test suite before continuing, adds a
  property-test subtask for each Correctness Property, and ends with a
  **Task Dependency Graph** (a JSON block of execution "waves") that
  `spec-execute` uses to pick the next unblocked task.

## Bugfix (three phases, like a feature spec)

```
/spec-bugfix <bug description>
  → bugfix.md (Current / Expected / Unchanged Behavior)   ── approve ──┐
                                                                       ▼
/spec-design <slug>
  → Bugfix Design: root cause, fix approach, and exactly
    three Properties to Test (bug reproducible, bug fixed,
    no regressions)                                       ── approve ──┐
                                                                       ▼
/spec-tasks <slug>
  → tasks.md, always including property tests for all
    three properties                                      ── approve ──┐
                                                                       ▼
/spec-execute <slug> [n]  → implements the fix, adds regression tests
```

`spec-bugfix` only captures the bug — current behavior, expected behavior,
and (importantly) the behavior that must stay unchanged, so the fix stays
surgical instead of turning into a rewrite. Root-cause investigation and
the fix approach happen in `spec-design` (it detects bugfix specs
automatically), and `spec-tasks` always generates the three required
property tests alongside the implementation task.

### Bugfix example

```
> /spec-bugfix login button does nothing on Safari

[bugfix.md drafted: Current/Expected/Unchanged Behavior — asks for approval]
> approved

> /spec-design login-button-safari

[investigates the code, drafts Bugfix Design with root cause, fix approach,
 and the three Properties to Test — asks for approval]
> approved

> /spec-tasks login-button-safari
[tasks.md drafted, including all three property tests — asks for approval]
> approved

> /spec-execute login-button-safari
[implements the fix, adds regression tests, reports]
```

## Quick Spec

```
/spec-quick <feature description>
  → asks 2-4 clarifying questions up front
  → generates requirements.md, design.md, and tasks.md back-to-back,
    with no approval gate between them
  → lands on the task list, ready to review or run /spec-execute
```

Same file formats as the gated workflows (it reads the same reference
templates rather than duplicating them) — just no per-phase review. Best
for small, well-understood features; reach for `/spec-new` instead if the
feature needs real review or turns out to be a bug report.

## Files this produces

```
docs/
├── steering/            (optional, from steering-setup)
│   ├── product.md
│   ├── tech.md
│   └── structure.md
└── specs/
    ├── <feature-slug>/
    │   ├── requirements.md
    │   ├── design.md
    │   └── tasks.md
    └── <bugfix-slug>/
        ├── bugfix.md
        ├── design.md
        └── tasks.md
```

## Plugin layout

```
spec-workflow/
├── commands/                         one thin file per skill — just points at it
└── skills/
    ├── spec-new/                     router: recommends a workflow, hands off
    ├── spec-requirements/
    │   ├── SKILL.md                  router: picks the mode below
    │   └── references/
    │       ├── template.md           shared Glossary + EARS structure
    │       ├── fresh-start.md        Requirements-First mode
    │       └── from-design.md        Design-First phase 2 mode
    ├── spec-design/
    │   ├── SKILL.md                  router: picks the mode below
    │   └── references/
    │       ├── feature-template.md   shared design.md structure
    │       ├── from-requirements.md  Mode A
    │       ├── design-first.md       Mode B (asks detail level)
    │       └── bugfix-design.md      Mode C (self-contained)
    ├── spec-bugfix/                  Bugfix Analysis phase (bugfix.md)
    ├── spec-tasks/
    │   ├── SKILL.md                  router: shared tasks.md shape
    │   └── references/
    │       ├── structure.md          hierarchy, checkpoints, dep graph
    │       ├── feature-tasks.md      requirement citations
    │       └── bugfix-tasks.md       bugfix citations, required PBTs
    ├── spec-quick/                   no-gate generator, reuses the above
    ├── spec-execute/                 implements tasks one at a time
    ├── spec-status/                  progress across all spec types
    └── steering-setup/               product/tech/structure context
```
