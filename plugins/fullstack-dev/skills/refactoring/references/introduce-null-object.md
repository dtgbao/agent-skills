# Introduce Null Object

**Category:** Simplifying Conditional Expressions  

## Problem

Many callers repeat the same absence check and perform the same default behavior.

## Refactoring

Provide an object implementing the neutral behavior and use it in place of null.

## Why use it

Make decision paths direct and keep variation from spreading through branches. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Do not use a null object to hide missing required data or failures that callers must distinguish. Preserve branch priority, short-circuit behavior, side effects, and error handling.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Define the common contract and the neutral behavior.
3. Create the null implementation.
4. Replace checks incrementally and keep explicit absence tests where absence itself matters.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Replace Conditional with Polymorphism](replace-conditional-with-polymorphism.md)
