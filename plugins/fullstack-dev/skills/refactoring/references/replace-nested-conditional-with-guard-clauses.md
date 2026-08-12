# Replace Nested Conditional with Guard Clauses

**Category:** Simplifying Conditional Expressions  

## Problem

Exceptional or prerequisite cases wrap the main path in deep nesting.

## Refactoring

Handle those cases first with guard clauses, leaving the normal path unindented.

## Why use it

Make decision paths direct and keep variation from spreading through branches. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Keep guards ordered when failures have priority, different messages, or observable side effects. Preserve branch priority, short-circuit behavior, side effects, and error handling.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify conditions that stop normal processing.
3. Move one case at a time to an early return or throw.
4. Flatten the remaining main path and consolidate equivalent guards.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
