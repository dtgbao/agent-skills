---
name: spec-quick
description: Generate requirements.md, design.md, and tasks.md for a feature in one continuous pass with no approval gates between phases. Use when the user says "/spec-quick", "quick spec", wants to move fast on a small well-understood feature, or explicitly doesn't want to review each phase separately.
argument-hint: "<feature description>"
---

# Spec Quick

Quick Spec trades the phase-by-phase review gates in the standard workflow
for speed: all three artifacts get generated back-to-back from a single
round of upfront questions. It reuses the exact same templates as the
gated skills — it does **not** duplicate them — so the output is
structurally identical to a spec built the slow way.

**When this fits:** a small, well-understood feature — a variant of
something already built many times — where you trust the output and don't
need to review requirements or design individually.

**When it doesn't:** compliance-sensitive domains, high-stakes systems,
unfamiliar territory, or anything where getting the requirements or
architecture wrong would be expensive. If the description sounds like it
needs real review, point the user to `/spec-new` or `/spec-requirements`
instead. If it sounds like a bug report rather than a feature, use
`/spec-bugfix` instead — bugfixes always go through the gated flow; there's
no quick variant for those.

## 1. Identify the spec

Derive a short kebab-case slug from `$ARGUMENTS`. Create
`.claude/specs/<slug>/`.

## 2. Ask clarifying questions up front — once

This replaces the per-phase back-and-forth. Ask 2-4 targeted questions
covering scope, constraints, and edge cases — whatever would materially
change the requirements, design, or task breakdown. If `$ARGUMENTS` is
already detailed enough that these are obvious, skip straight to Step 3
with minimal or no questions; don't ask questions whose answers you can
already infer confidently.

## 3. Generate all three artifacts, back-to-back, with no gates

Using the description and answers, produce each file in order, writing
each to disk before moving to the next. Read the same reference files the
gated skills use:

- `${CLAUDE_PLUGIN_ROOT}/skills/spec-requirements/references/template.md`
  for requirements.md (Glossary + EARS)
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-design/references/feature-template.md`
  for design.md
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-tasks/references/structure.md` and
  `references/feature-tasks.md` for tasks.md

**Skip every "present and gate" / "wait for approval" instruction in those
reference files** — that's the one thing Quick Spec intentionally omits.
Generate requirements.md first, then design.md from it (citing requirement
numbers as normal, since they now exist), then tasks.md from both, writing
each to `.claude/specs/<slug>/` as you go, without pausing for confirmation
in between.

Because there's no review checkpoint to catch a wrong turn mid-way, ground
each artifact as carefully as you would normally — the clarifying answers
from Step 2 are what stand in for the review gates, so use them fully
rather than filling gaps with assumptions.

## 4. Land on the task list

Once all three files are written, show the task list (or a concise summary
plus a pointer to `tasks.md`) and tell the user all three files are saved
and reviewable/editable like any other spec. Mention they can start
implementation directly with `/spec-execute <slug>`, or ask for changes to
any of the three files first.
