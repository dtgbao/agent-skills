# Decompose Conditional

**Category:** Simplifying Conditional Expressions  

## Problem

A condition and its branches contain enough detail to hide the decision's intent.

## Refactoring

Extract the condition and branch actions into well-named functions.

## Why use it

Make decision paths direct and keep variation from spreading through branches. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Extraction should reveal the business decision, not merely relocate opaque code. Preserve branch priority, short-circuit behavior, side effects, and error handling.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Name and extract the predicate.
3. Extract each substantial branch by its outcome.
4. Keep the controlling conditional as a short statement of policy.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
