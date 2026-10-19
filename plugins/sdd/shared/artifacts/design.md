# design.md (feature)

Bugfix → `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/bugfix-design.md`. Views per `${CLAUDE_PLUGIN_ROOT}/shared/visuals.md`.

Done when:
- every criterion maps to ≥1 component (`_Requirements: x.y_` on component) or property. Design-First: filled when requirements are derived
- every new or changed component has interface sketch in project language (signature or type)
- every external dependency has Error Handling entry
- ≥1 Mermaid diagram
- File/Folder Structure is a `diff` file tree
- every component whose control flow changes shows call tree (or call-stack change) as `diff`
- Criteria Classification lists every criterion (`${CLAUDE_PLUGIN_ROOT}/shared/correctness.md` step 2)
- Testing Strategy lists every Property N in this file: generator, iterations
- Testing Strategy lists the seams: each public interface tests drive, with what it catches and what it misses. Tasks test only at these seams
- every non-functional constraint (latency, security, compliance) has owner component
- every `## Open Questions` item in requirements is decided under Key design decisions or marked out of scope

Skeleton:

```markdown
# Design Document: <feature>

## Overview

<approach, 1 paragraph>

**Key design decisions:**
- <decision>: <reason>

## Architecture

<mermaid diagram + request/data flow, numbered>

## File/Folder Structure

<file tree as `diff`, one-line role per entry>

## Components and Interfaces

### <Component> (`<path>`)

<responsibility>

<interface sketch in project language>

<call tree / call-stack change as `diff`, when control flow changes>

_Requirements: x.y_

## Data Models

<schemas, env vars, types>

## Criteria Classification

| Criterion | Class | Property |
|---|---|---|
| 1.1 | invariant | 1 |

## Correctness Properties

### Property N: <title>

*For any* <inputs with precondition>, <system> SHALL <invariant>.

**Validates: Requirements x.y**

## Error Handling

<per failure: cause, behavior, user-visible result>

## Testing Strategy

<unit, property, integration; library>

| Seam | Catches | Misses |
|---|---|---|
| `<public interface>` | <behavior it proves> | <what it cannot see> |

| Property | Generators | Iterations |
|---|---|---|
| 1 | <arbitraries> | ≥100 |
```
