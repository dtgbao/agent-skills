# design.md template (feature specs — Modes A and B)

## Structure

```markdown
# Design Document: <Feature Name>

## Overview
<How this fits into the existing system, in 2-4 sentences>

**Key design decisions:**
- <A significant technical choice and why, e.g. library vs. custom
  implementation, storage backend, where logic lives>
- <Another decision and its tradeoff>

## Architecture
<High-level approach. Include a Mermaid diagram (```mermaid) for anything
with more than 2-3 moving parts — component/sequence/flow diagram as
appropriate.>

**Request flow:** (or the equivalent walkthrough for non-request-driven
features)
1. <Step-by-step numbered walkthrough of the diagram above>
2. ...

## Components and Interfaces
<One `###` subsection per component/module. For each: its responsibility, a
short code block showing its actual interface/signature/usage, and a table
where structured data (e.g. response headers, config options) is clearer as
a table than prose.>

## Data Models
<One `###` subsection per distinct data concern — e.g. environment
variables, schemas/types, storage key structure. Use tables for
variable/field lists and code blocks for type definitions.>

## Correctness Properties  <!-- optional — see guidance below -->
<Universal properties the implementation must satisfy, each stated
precisely enough to drive a property-based test.>

## Error Handling
<One `###` subsection per error scenario/category: what triggers it, how
the system responds, and any mitigation.>

## Testing Strategy
<See structure below.>
```

## Correctness Properties — when to include it

Include this section when the feature has behavior that's more naturally
verified as a universal rule across many inputs than as a handful of
examples — rate limits, parsers, validators, state machines, anything with
"for all X, Y must hold" logic. Skip it for features that are essentially
wiring/CRUD with no such invariants; don't force properties into a design
that doesn't have any.

When included, open with a one-line definition of what a property is (a
behavior that holds across all valid executions, not just specific
examples), then list each as:

```markdown
### Property 1: <short title>

*For any* <universally-quantified input(s)>, <the guaranteed behavior,
stated precisely enough to assert in a test>.

**Validates: Requirements X.Y, X.Z**

---
```

Every property should map back to one or more acceptance criteria (Mode A)
or to the design's own guarantees (Mode B, before requirements exist —
reference them loosely by capability and reconcile the numbering once
`spec-requirements` derives the requirement numbers). These properties are
what `spec-tasks` will turn into property-based test tasks, so state them
as something a `fast-check` (or equivalent) test could literally assert.

## Testing Strategy structure

```markdown
## Testing Strategy

### Dual testing approach
<Short paragraph: unit tests for specific examples/edge cases, property-based
tests for the universal properties above, if any. Name the PBT library.>

### Unit tests

| Test | Description |
|---|---|
| ... | ... |

### Property-based tests (<library>)  <!-- omit if no Correctness Properties -->
Each property test runs a **minimum of 100 iterations**.

**Tag format:** `// Feature: <feature-slug>, Property {N}: {property_text}`

| Property | Generators | Assertion |
|---|---|---|
| ... | ... | ... |

### Integration / smoke tests

| Test | Description |
|---|---|
| ... | ... |
```

## General guidance

Every non-trivial design decision should trace back to a requirement (Mode
A) or an explicit user-stated goal (Mode B) — reference requirement numbers
where it clarifies why something exists (Mode A only, since Mode B has no
requirement numbers yet). If a requirement turns out ambiguous or
under-specified once you try to design against it, flag it explicitly
rather than silently resolving it your own way. Follow conventions from
`.claude/steering/tech.md` and `structure.md` where they exist (naming,
folder layout, preferred libraries) rather than introducing new patterns.
