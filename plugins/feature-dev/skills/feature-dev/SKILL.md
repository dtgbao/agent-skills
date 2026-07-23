---
name: feature-dev
description: Guided feature development with codebase understanding and architecture focus
---

# Feature Development

You are helping a developer implement a new feature. Follow a systematic approach: understand the codebase deeply, identify and ask about all underspecified details, design elegant architectures, then implement.

## Core Principles

- **Ask clarifying questions**: Identify all ambiguities, edge cases, and underspecified behaviors. Ask specific, concrete questions rather than making assumptions. Wait for user answers before proceeding with implementation. Ask questions early (after understanding the codebase, before designing architecture).
- **Understand before acting**: Read and comprehend existing code patterns first
- **Read files identified by agents**: When launching agents, ask them to return lists of the most important files to read. After agents complete, read those files to build detailed context before proceeding.
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

1. Launch one subagent using `assets/templates/code-explorer.toml` as its prompt template. The subagent should:
   - Trace through the code comprehensively and focus on getting a comprehensive understanding of abstractions, architecture and flow of control
   - Target a different aspect of the codebase (eg. similar features, high level understanding, architectural understanding, user experience, etc)
   - Include a list of key files to read

   **Example agent prompts**:
   - "Find features similar to [feature] and trace through their implementation comprehensively"
   - "Map the architecture and abstractions for [feature area], tracing through the code comprehensively"
   - "Analyze the current implementation of [existing feature/area], tracing through the code comprehensively"
   - "Identify UI patterns, testing approaches, or extension points relevant to [feature]"

2. Once the agent returns, please read all files to build deep understanding
3. Present comprehensive summary of findings and patterns discovered

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

1. Launch one subagent using `assets/templates/code-architect.toml` as its prompt template and ask it to compare these focuses: minimal changes (smallest change, maximum reuse), clean architecture (maintainability, elegant abstractions), and pragmatic balance (speed + quality)
2. Review the approaches and form your opinion on which fits best for this specific task (consider: small fix vs large feature, urgency, complexity, team context)
3. Present to user: brief summary of each approach, trade-offs comparison, **your recommendation with reasoning**, concrete implementation differences
4. **Ask user which approach they prefer**

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
6. Write clean, well-documented code
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
