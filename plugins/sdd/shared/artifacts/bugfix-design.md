# design.md (bugfix)

Views per `${CLAUDE_PLUGIN_ROOT}/shared/visuals.md`. No Criteria Classification: Property 1 and 2 cover the behavior criteria. Interface-level criterion (signature, error type, config) → example-only: name its example test in Regression Strategy, not a property.

Done when:
- Root Cause cites `file:line`, explains every Current item; each cite checked with `grep -n` before the gate
- Fix names every changed component and its constraint
- Call-tree Change shows the failing path as `diff`
- Property 1 = fix check, Property 2 = preservation, each with `**Validates:**`
- Regression Strategy names the pin tests for every Unchanged item and the example test for every example-only criterion

Skeleton:

```markdown
# Design Document: <bug>

## Root Cause

<cause, evidence `file:line`>

## Fix

<change, affected components, constraints>

### Call-tree Change

<`diff` of the failing call path>

## Correctness Properties

### Property 1: Fix check

*For any* input where bug condition holds, <system> SHALL <expected>.

**Validates: Requirements 2.x**

### Property 2: Preservation

*For any* input where bug condition fails, <system> SHALL <unchanged>.

**Validates: Requirements 3.x**

## Regression Strategy

<seams the pins drive; pin tests: exploration (red before fix, holds Property 1), preservation (green before fix, one holds Property 2)>
```
