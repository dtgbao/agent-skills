---
name: spec-new
description: Start a new spec and pick the right workflow for it. Use when the user wants to start a new feature or fix, says "start a spec", "new feature", "let's build X", "I found a bug", or is unsure which spec workflow to use. Recommends Requirements-First, Design-First, Bugfix, or Quick Spec based on the request, and hands off to the matching skill once the user confirms.
argument-hint: "<what you want to build or fix>"
---

# Spec New

This is the front door to the whole spec workflow. Its only job is to figure
out which of the four workflows fits, get the user's confirmation, and hand
off — it doesn't draft any spec content itself.

## 0. Get a description to work with

If `$ARGUMENTS` is empty or too vague to reason about (e.g. just "help me
plan something"), ask what they want to build or fix before doing anything
else.

## 1. Recommend a workflow

Weigh the description against these four workflows and pick the best fit.
Each maps to a distinct skill in this plugin:

| Workflow | Best for | Skill |
|---|---|---|
| **Requirements-First** | Clear user-facing behavior, flexible/undetermined technical approach, greenfield work | `spec-requirements` |
| **Design-First** | A known tech stack, strict non-functional requirements (latency/throughput/uptime/compliance), an existing architecture/diagram to port in, or feasibility exploration with strong architectural opinions | `spec-design` |
| **Bugfix** | Something already built is behaving incorrectly — a bug report, regression, or crash | `spec-bugfix` |
| **Quick Spec** | A small, well-understood, low-risk feature — a variant of something you've built many times, where you trust the output and don't need to review each phase | `spec-quick` |

Signals to weigh, roughly in priority order:

1. **Describes broken existing behavior** ("X is broken", "getting an error
   when...", "used to work, now it doesn't", "regression") → **Bugfix**,
   regardless of other signals.
2. **Leads with specific technology, services, or hard numbers** ("using
   Postgres and Redis", "must handle 10k req/s", "99.99% uptime", "must
   comply with SOC 2", references an uploaded diagram/design doc) →
   **Design-First**.
3. **Explicitly wants speed over review**, or describes something small and
   routine ("just add a...", "quick", "small tweak", "you know the drill",
   "don't need me to review each step") → **Quick Spec**.
4. **Everything else** — clear-enough behavior, no strong technical
   opinions yet, not trivial — → **Requirements-First** (the safe default).

## 2. Present the recommendation and ask

State your recommendation with a one-line reason, then list all four
options briefly so the user can override it. For example:

> Based on "<short paraphrase>", I'd recommend **Requirements-First** — the
> behavior is clear but the technical approach is still open. Other
> options: **Design-First** (if you already have a stack/architecture in
> mind), **Bugfix** (if this is actually fixing something broken), or
> **Quick Spec** (if you'd rather skip the review gates for something this
> straightforward). Which would you like?

Wait for their answer. Don't proceed on the recommendation without an
explicit go-ahead — that's the one approval gate this skill itself owns.

## 3. Hand off

Once the user picks (or confirms your recommendation), immediately read and
follow the corresponding skill file, passing the original description (plus
anything they added while discussing the choice) as its input — don't make
them repeat themselves in a separate command:

- Requirements-First → `${CLAUDE_PLUGIN_ROOT}/skills/spec-requirements/SKILL.md`
- Design-First → `${CLAUDE_PLUGIN_ROOT}/skills/spec-design/SKILL.md`
- Bugfix → `${CLAUDE_PLUGIN_ROOT}/skills/spec-bugfix/SKILL.md`
- Quick Spec → `${CLAUDE_PLUGIN_ROOT}/skills/spec-quick/SKILL.md`

Continue directly into that skill's own steps (e.g. deriving a slug,
building a glossary, asking its own clarifying questions) — `spec-new`'s job
ends at a confident handoff.
