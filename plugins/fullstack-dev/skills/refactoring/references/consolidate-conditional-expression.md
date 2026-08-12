# Consolidate Conditional Expression

**Category:** Simplifying Conditional Expressions  

## Problem

Several checks lead to the same result but are expressed as separate branches.

## Refactoring

Combine them into one named predicate and one outcome branch.

## Why use it

Make decision paths direct and keep variation from spreading through branches. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Combining conditions can alter short-circuit order or conceal checks that differ for a reason. Preserve branch priority, short-circuit behavior, side effects, and error handling.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Verify the branches truly have the same outcome.
3. Combine conditions while preserving evaluation order.
4. Extract the combined predicate when a name improves meaning.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
