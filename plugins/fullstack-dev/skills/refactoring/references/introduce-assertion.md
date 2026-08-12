# Introduce Assertion

**Category:** Simplifying Conditional Expressions  

## Problem

Code depends on an internal assumption that is not documented or checked.

## Refactoring

Express the assumption with an assertion close to where it must hold.

## Why use it

Make decision paths direct and keep variation from spreading through branches. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Assertions document programmer invariants; they do not replace validation for user input or recoverable errors. Preserve branch priority, short-circuit behavior, side effects, and error handling.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. State the invariant precisely.
3. Add the assertion before code that relies on it.
4. Confirm production assertion behavior matches the project's runtime policy.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
