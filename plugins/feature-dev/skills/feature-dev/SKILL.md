---
name: feature-dev
description: Guided feature development with codebase understanding and architecture focus
---

# Feature Development

You are helping a developer implement a new feature. Follow a systematic approach: understand the codebase deeply, identify and ask about all underspecified details, design elegant architectures, then implement.

## Core Principles

- **Ask clarifying questions**: Identify all ambiguities, edge cases, and underspecified behaviors. Ask specific, concrete questions rather than making assumptions. Wait for user answers before proceeding with implementation. Ask questions early (after understanding the codebase, before designing architecture).
- **Understand before acting**: Read and comprehend existing code patterns first
- **Exploration**: Read the relevant implementation, tests, configuration, and documentation to build detailed context
- **Simple and elegant**: Prioritize readable, maintainable, architecturally sound code
- **Use TodoWrite**: Track all progress throughout

---

## Phase 1: Discovery

**Goal**: Understand what needs to be built

**Actions**:

1. Create todo list with all phases
2. If feature unclear, ask user for:
   - What problem are they solving?
   - What should the feature do?
   - Any constraints or requirements?
3. Summarize understanding and confirm with user

---

## Phase 2: Codebase Exploration

**Goal**: Understand relevant existing code and patterns at both high and low levels

**Actions**:

1. Read [codebase-exploration](references/codebase-exploration.md) and apply it directly until its completion criterion holds
2. Present a comprehensive summary of the findings, patterns, and essential files

---

## Phase 3: Clarifying Questions

**Goal**: Fill in gaps and resolve all ambiguities before designing

**CRITICAL**: This is one of the most important phases. DO NOT SKIP.

**Actions**:

1. Read [$grilling](../grilling/SKILL.md) skill and follow its questioning guidance throughout this phase
2. If `docs/adr/` exists, also read [$domain-modeling](../domain-modeling/SKILL.md) and run the grilling session using its domain-modeling guidance
3. Review the codebase findings and original feature request
4. Identify underspecified aspects: edge cases, error handling, integration points, scope boundaries, design preferences, backward compatibility, performance needs
5. Ask one question at a time, provide a recommended answer, and wait for the user's response before continuing
6. Confirm shared understanding before proceeding to architecture design

If the user says "whatever you think is best", provide your recommendation and get explicit confirmation.

---

## Phase 4: Architecture Design

**Goal**: Design multiple implementation approaches with different trade-offs

**Actions**:

1. Ask the user to choose a plan output: no artifact, Markdown, or HTML. Wait for their decision before continuing
2. Read [architecture-design](references/architecture-design.md) and apply it directly until its completion criterion holds
3. If the user chose Markdown or HTML, create the complete plan at `docs/plans/YYYY-MM-DD-<feature-name>.{md,html}` using the selected extension. For HTML, first read [$html-plan](../html-plan/SKILL.md)
4. Present the approach comparison, **your recommendation with reasoning**, implementation differences, and artifact path when created
5. **Ask the user which approach they prefer**

---

## Phase 5: Implementation

**Goal**: Build the feature

**DO NOT START WITHOUT USER APPROVAL**

**Actions**:

1. Wait for explicit user approval
2. Read [$tdd](../tdd/SKILL.md) skill and follow its test-driven development workflow throughout this phase
3. Read all relevant files identified in previous phases
4. Confirm the public seams to test, then implement the chosen architecture in red-green vertical slices
5. Follow codebase conventions strictly
6. Run type checking, single test files, and linting regularly. Run the full test suite and format the code once at the end
7. Update todos as you progress

---

## Phase 6: Code Review

**Goal**: Ensure the changes follow repository standards and the feature specification

**Actions**:

1. Read [$code-review](../code-review/SKILL.md) completely
2. Follow its two-axis review process, including launching the Standards and Spec subagents in parallel
3. Present the two reports separately without merging or reranking their findings
4. **Ask the user what they want to do** (fix now, fix later, or proceed as-is)
5. Address issues based on user decision

---

## Phase 7: Summary

**Goal**: Document what was accomplished

**Actions**:

1. Mark all todos complete
2. Summarize:
   - What was built
   - Key decisions made
   - Files modified
   - Suggested next steps

---
