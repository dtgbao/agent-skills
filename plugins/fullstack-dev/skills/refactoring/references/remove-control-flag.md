# Remove Control Flag

**Category:** Simplifying Conditional Expressions  

## Problem

A Boolean variable exists mainly to escape or suppress further loop processing.

## Refactoring

Use structured control flow such as return, break, or continue instead of the flag.

## Why use it

Make decision paths direct and keep variation from spreading through branches. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Preserve cleanup, finally behavior, and the exact scope exited by the replacement statement. Preserve branch priority, short-circuit behavior, side effects, and error handling.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Find assignments that only signal control flow.
3. Replace each with the narrowest structured exit.
4. Remove the flag and simplify conditions that referenced it.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
