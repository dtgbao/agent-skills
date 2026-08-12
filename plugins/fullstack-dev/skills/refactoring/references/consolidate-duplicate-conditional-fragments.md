# Consolidate Duplicate Conditional Fragments

**Category:** Simplifying Conditional Expressions  

## Problem

The same statement appears in every branch of a conditional.

## Refactoring

Move the shared statement before or after the conditional as its dependencies require.

## Why use it

Make decision paths direct and keep variation from spreading through branches. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Do not move code across a branch boundary when timing, exceptions, or mutated values differ. Preserve branch priority, short-circuit behavior, side effects, and error handling.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Confirm the fragments are behaviorally identical.
3. Choose a location where required values are available.
4. Move one shared fragment and simplify the branches.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
