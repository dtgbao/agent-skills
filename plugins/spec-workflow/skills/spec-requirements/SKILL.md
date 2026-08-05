---
name: spec-requirements
description: Start Requirements-First on a new feature, revise an existing requirements.md, or derive requirements from an already-approved design.md (Design-First phase 2). Use when the user wants to plan a new feature, says "create a spec for X", "let's spec out X", or asks to update/revise requirements for an existing spec.
argument-hint: "<feature-name or description> [revision notes]"
---

# Spec Requirements

Requirements are always the artifact reviewed first, but not always the
artifact *written* first — see Step 1 to find your mode, then read the
matching reference file before drafting anything. Regardless of mode, do
not proceed to the next phase in this skill — that happens only after the
user explicitly approves requirements.md.

## 0. Load context

If `docs/steering/product.md`, `tech.md`, or `structure.md` exist, read
them for product and technical context before drafting anything.

## 1. Identify the spec and the mode

Derive a short kebab-case feature slug from `$ARGUMENTS` (e.g. "user
authentication" → `user-authentication`), unless one is already implied by
an existing spec directory. Check `docs/specs/<slug>/`:

- **`requirements.md` already exists** → **revision**. Read the current
  file and `references/template.md`, treat `$ARGUMENTS` as the requested
  change, and keep existing glossary terms and numbering stable for
  anything you're not touching. The next phase after saving is
  `spec-design` if no design.md exists yet, otherwise `spec-tasks`.
- **No `requirements.md`, but `design.md` exists** → **Design-First phase
  2.** Read `references/from-design.md`, then `references/template.md`.
- **Neither exists** → **fresh Requirements-First start.** Create
  `docs/specs/<slug>/`. Read `references/fresh-start.md`, then
  `references/template.md`.

If the feature description is too vague to write meaningful requirements
(e.g. just "add auth"), ask up to 2-3 targeted clarifying questions before
drafting — don't guess at product decisions that materially change scope.

## 2. Draft, present, and gate

Follow the mode-specific reference file for how to gather content and what
comes next, and `references/template.md` for the exact structure and EARS
rules. Show the drafted (or revised) requirements.md content in full and
end with:

> Do these requirements look right? Reply with changes, or say "approved" /
> "looks good" to move on to `<the correct next phase per Step 1>`.

**Wait for explicit approval before considering this phase done.** If the
user asks for changes, revise and re-present — don't move to the next phase
yourself even if the changes look complete to you.

## 3. On approval

Write the final content to `docs/specs/<slug>/requirements.md`. Tell the
user it's saved and name the correct next command per Step 1: `/spec-design
<slug>` (fresh start) or `/spec-tasks <slug>` (Design-First — design
already exists).
