# design.md

Done when:
- every criterion maps to ≥1 component or property (cite `_Requirements: x.y_` on component)
- every external dependency has Error Handling entry
- every component has interface sketch (signature or type)
- ≥1 Mermaid diagram
- File/Folder Structure shows the file tree as a `diff` block
- every changed component shows its component tree or call tree (or call-stack change) as a `diff` block; views per `${CLAUDE_PLUGIN_ROOT}/shared/visuals.md`
- Testing Strategy lists every property from `${CLAUDE_PLUGIN_ROOT}/shared/correctness.md`
- every non-functional constraint (latency, security, compliance) has an owner component

Skeleton (feature):

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

<responsibility, interface sketch>

<component tree or call tree / call-stack change as `diff`>

_Requirements: x.y_

## Data Models

<schemas, env vars, types>

## Correctness Properties

### Property N: <title>

*For any* <inputs with precondition>, <system> SHALL <invariant>.

**Validates: Requirements x.y**

## Error Handling

<per failure: cause, behavior, user-visible result>

## Testing Strategy

<unit, property, integration; library; iteration count>
```

Skeleton (bugfix) — replace middle sections:

```markdown
## Root Cause

<cause, evidence `file:line`>

## Fix

<change, affected components, constraints>

### Call-tree change

<`diff` of the failing call path per `${CLAUDE_PLUGIN_ROOT}/shared/visuals.md`>

## Validation Properties

- Fix check: *for any* input where bug condition holds, <system> SHALL <expected>.
- Preservation: *for any* input where bug condition fails, <system> SHALL <unchanged>.

## Regression Strategy

<what pins existing behavior>
```
