# Replace Conditional with Polymorphism

**Category:** Simplifying Conditional Expressions  

## Problem

Type- or variant-based branching is repeated and grows whenever a new behavior is added.

## Refactoring

Move each variant's behavior behind a common operation implemented polymorphically.

## Why use it

Make decision paths direct and keep variation from spreading through branches. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

A single stable conditional may be clearer than a hierarchy; use polymorphism only when variation is real. Preserve branch priority, short-circuit behavior, side effects, and error handling.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify the common operation represented by the branches.
3. Introduce or reuse a suitable abstraction for the variants.
4. Move one branch at a time into implementations and replace the conditional with dispatch.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
