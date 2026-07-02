---
name: prd-to-plan
description: Use when turning a PRD, requirements doc, product spec, user stories, or acceptance criteria into an engineering plan, implementation plan, technical plan, task breakdown, or test plan.
---

# PRD to Plan

Use this skill to turn a PRD into a practical implementation plan without skipping codebase discovery or the architecture conversation. The workflow has four phases:

1. Understand the PRD
2. Explore the codebase against the requirements
3. Design the architecture and get approval
4. Write the detailed implementation plan

The approval gate matters because a detailed plan encodes architecture decisions deeply. Do not write the detailed implementation plan until the user approves an architecture approach.

## Inputs

Accept any of these as the PRD source:

- A Jira, GitHub, Linear, or project issue containing a PRD
- A Markdown, Google Doc, text file, or pasted PRD
- Conversation context that clearly includes PRD sections

If the PRD location is missing, ask for it. If the PRD content is present but ambiguous, proceed with explicit assumptions and call out the uncertain parts in the architecture proposal.

## Required Skills

Use these skills in order:

1. `grill-with-docs` during architecture design
2. `writing-plans` after the user approves an architecture approach

If the repository has its own agent instructions, follow them as well. If they require reading conventions, glossary, ADR, or testing documents before planning, read those before proposing architecture.

## Phase 1: Understand the PRD

Read the PRD and extract:

- Problem statement
- Solution summary
- Actors and user stories
- Acceptance criteria
- Implementation decisions already made
- Testing decisions already made
- Out of scope items
- Open questions or missing constraints

Respect the PRD's intent:

- Use domain glossary vocabulary from the repo.
- Treat implementation decisions as constraints unless code or docs contradict them.
- Treat testing decisions as starting points, not as the complete test plan.
- Do not add file paths to the PRD itself; file paths belong in the implementation plan.

## Phase 2: Codebase Exploration

**Goal:** Understand the relevant existing code and patterns at both high and low levels, then check the PRD requirements against what the system actually supports.

Explore the codebase yourself. Do not launch a subagent for this phase.

Use the PRD summary to drive one comprehensive investigation covering:

- Similar features and reusable implementation patterns
- High-level architecture, domain boundaries, abstractions, dependencies, and control flow
- User experience, UI patterns, state management, API boundaries, persistence, outputs, and extension points
- Existing testing approaches, fixtures, seams, and relevant failure handling

Complete these steps before proposing architecture:

1. Search for similar features, names, routes, components, models, tests, and docs.
2. Read every relevant file needed to verify behavior. Do not rely on search snippets alone.
3. Trace control flow from entry points through state, APIs, persistence, side effects, and outputs.
4. Follow directly referenced files when needed to verify abstractions, boundaries, or requirements.
5. Compare existing behavior with every relevant user story and acceptance criterion.
6. Identify reusable patterns, constraints, extension points, gaps, risks, and contradictions.
7. Resolve conflicting findings against the code and documented decisions.
8. Build a key-file list with a reason for each file read.

Present this summary before proposing architecture:

```markdown
## Codebase Exploration Summary

### Existing Architecture and Control Flow
[Relevant high-level architecture and traced low-level flow.]

### Patterns and Extension Points
[Reusable modules, interfaces, UI patterns, test seams, and conventions.]

### Requirements Fit
| User story / AC | Existing support | Required change | Evidence |
|---|---|---|---|

### Constraints, Gaps, and Risks
[Contradictions, missing capabilities, migration concerns, failure modes, and unclear requirements.]

### Key Files Read
| File | Why it matters |
|---|---|
```

Use this evidence as the basis for architecture options. Prefer answering questions by reading code and docs before asking the user.

## Phase 3: Architecture Proposal

Announce that you are using `grill-with-docs` to challenge the PRD against the existing domain model and documented decisions.

Produce an architecture proposal with this exact structure:

````markdown
# Architecture Proposal: [Feature Name]

## PRD Coverage Summary
- User stories covered: [count and short list]
- Acceptance criteria covered: [count and short list]
- Edge cases identified: [count and short list]
- Error paths identified: [count and short list]
- Out of scope preserved: [short list]

## Existing System Context
- Domain terms: [canonical terms and any conflicts]
- Existing modules and seams: [brief list]
- Relevant docs and ADRs: [brief list]
- Constraints from code: [brief list]

## Approach 1: [Name]
- Design:
- Covers:
- Trade-offs:
- Risks:
- Best fit when:

## Approach 2: [Name]
- Design:
- Covers:
- Trade-offs:
- Risks:
- Best fit when:

## Approach 3: [Name]
- Design:
- Covers:
- Trade-offs:
- Risks:
- Best fit when:

## Recommended Approach
- Recommendation: [one approach]
- Rationale:
- Trade-offs accepted:
- Trade-offs rejected:
- Required clarifications:

## Mermaid Diagram
```mermaid
[diagram for the recommended approach]
```

## Approval Gate
Do you approve the recommended architecture approach so I can proceed to the detailed implementation plan?
````

Use two approaches when the design space is genuinely small. Use three when there are meaningful alternatives. Do not pad with fake options.

### Coverage Requirements

For every user story and acceptance criterion, ensure the proposal names where it is handled. Include:

- Happy paths
- Empty states
- Loading states
- Permission or authorization failures
- Validation failures
- API/network failures
- Data consistency issues
- Race conditions or stale data
- Backward compatibility and migrations when relevant
- Observability, analytics, or audit implications when relevant

### Grill-With-Docs Behavior

Use the spirit of `grill-with-docs` before asking the user:

- Check the repo glossary, docs, ADRs, and code for answers first.
- Challenge fuzzy terms and propose canonical terms.
- Surface contradictions between the PRD and code.
- Ask one question at a time only when the answer cannot be discovered locally.
- Provide your recommended answer with each question.

If a domain term is resolved during the planning conversation and the repo has a `CONTEXT.md`, update it only when the user confirms the term. Keep glossary updates free of implementation details.

Offer an ADR only when the decision is hard to reverse, surprising without context, and the result of a real trade-off.

## Stop Before Detailed Planning

After the architecture proposal, stop and wait for explicit approval.

Do not proceed on vague replies like "interesting", "maybe", or "continue discussing". Proceed only on clear approval such as "approved", "go with approach 2", "proceed", or an equivalent directive.

If the user changes the architecture choice, update the proposal first, including the mermaid diagram, then ask for approval again.

## Phase 4: Detailed Implementation Plan

After approval, announce: "I'm using the writing-plans skill to create the implementation plan."

Save the plan to:

```text
docs/plans/YYYY-MM-DD-<feature-name>.md
```

Use the repo's preferred plan location if its instructions specify one.

Use the approved architecture as the source of truth, then read `references/detailed-implementation-plan.md` for the PRD-specific plan sections and self-review checks.
