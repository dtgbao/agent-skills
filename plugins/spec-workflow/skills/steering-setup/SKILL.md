---
name: steering-setup
description: Set up or refresh persistent project context for this spec-driven workflow. Use when the user asks to "set up steering", "initialize project context for specs", starts using this workflow for the first time in a repo, or when product/tech/structure context seems stale. Creates .claude/steering/product.md, tech.md, and structure.md.
argument-hint: "[what changed, e.g. 'we switched to Postgres']"
---

# Steering Setup

Steering documents give every other skill in this workflow durable, repo-specific
context so you don't have to re-explain your product, stack, and conventions in
every spec.

## What to produce

Create (or update) three files under `.claude/steering/`:

1. **product.md** — What the product is, who it's for, and the key features/goals.
   2-4 short sections is enough; this is not a full PRD.
2. **tech.md** — Language(s), frameworks, key libraries, build/test/lint commands,
   deployment target, and any hard constraints (e.g. "no new npm dependencies
   without approval", "must support Node 18+").
3. **structure.md** — How the repo is organized: top-level folders and what lives
   where, naming conventions, where tests live relative to source.

## How to gather the content

1. If `.claude/steering/` already has these files, read them first and treat this
   as an update, not a rewrite — preserve anything still accurate.
2. Inspect the repo to ground the docs in reality rather than guessing: check
   `package.json` / `pyproject.toml` / `go.mod` / etc. for stack and scripts, skim
   the top-level directory listing, check for a README, and check for existing
   lint/test config.
3. If the user provided arguments (`$ARGUMENTS`), treat that as an explicit update
   instruction (e.g. "we switched to Postgres") and apply it.
4. Ask the user directly only for things you genuinely can't infer from the repo —
   for example the target audience or product goals rarely live in code. Keep
   questions to the minimum needed; don't block on things you can reasonably infer.

## Format

Keep each file short — a few hundred words, not a document. Use plain prose and
short bullet lists. These files get read by every other skill in this workflow,
so brevity keeps token cost down across the whole spec process.

## After writing

Confirm the three files are in place and give the user a one-line summary of what
each now says. Let them know they can run this skill again any time the product,
stack, or repo layout changes meaningfully.
