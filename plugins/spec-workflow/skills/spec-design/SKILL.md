---
name: spec-design
description: Produce a technical design — either derived from an approved requirements.md, started fresh as a Design-First entry point, or as the root-cause/fix design for a bugfix spec. Use when the user asks to design a feature, says "let's do the design phase", "/spec-design", "design a system that...", or wants to revise an existing design.md.
argument-hint: "<feature-slug or new feature/design description> [notes or revision request]"
---

# Spec Design

Design is always reviewed as its own phase, but which phase it *is* — and
which template applies — depends on how the spec started. See Step 1 to
find your mode, then read the matching reference file before drafting
anything. Regardless of mode, do not generate tasks.md in this skill —
that happens only after the user explicitly approves this design, via
`spec-tasks`.

## 0. Load context

Read `.claude/steering/*.md` if present, for product/tech/structure
context.

## 1. Identify the spec and the mode

Derive a short kebab-case slug from `$ARGUMENTS` if one isn't already
implied by an existing spec directory. Check `.claude/specs/<slug>/`:

- **`design.md` already exists** → **revision**. Read it, then infer the
  original mode from what's alongside it (`requirements.md` → Mode A,
  `bugfix.md` → Mode C, neither → Mode B) and read that mode's reference
  file to reapply the right structure while treating `$ARGUMENTS` as the
  requested change.
- **No `design.md`, and `requirements.md` exists** → **Mode A: derive
  design from requirements.** Read `references/from-requirements.md`, then
  `references/feature-template.md`.
- **No `design.md`, and `bugfix.md` exists (no `requirements.md`)** →
  **Mode C: bugfix design.** Read `references/bugfix-design.md` — it's
  self-contained, no need for `feature-template.md`.
- **Neither `requirements.md` nor `bugfix.md` exists** → **Mode B:
  Design-First entry**, the first artifact for this spec. Create
  `.claude/specs/<slug>/`. Read `references/design-first.md`, then
  `references/feature-template.md`.

## 2. Draft, present, and gate

Follow the mode-specific reference file for how to gather content and what
comes next, plus (Modes A/B) `references/feature-template.md` for the
exact design.md structure. Show the full design.md content and end with:

> Does this design look right? Reply with changes, or say "approved" to
> move on to `<the correct next phase per the mode's reference file>`.

Wait for explicit approval. Revise and re-present on request rather than
proceeding unprompted.

## 3. On approval

Write the final content to `.claude/specs/<slug>/design.md`. Tell the user
it's saved and name the correct next command: `/spec-requirements <slug>`
(Mode B) or `/spec-tasks <slug>` (Modes A and C).
