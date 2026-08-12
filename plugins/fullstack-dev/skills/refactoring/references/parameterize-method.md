# Parameterize Method

**Category:** Simplifying Method Calls  

## Problem

Several methods perform the same operation with only a literal or small choice changed.

## Refactoring

Replace them with one method whose parameter represents the variation.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Do not parameterize genuinely different responsibilities or create an opaque mode flag. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify the single dimension that varies.
3. Introduce a parameter with a meaningful domain type.
4. Replace duplicate methods and migrate callers.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Replace Parameter with Explicit Methods](replace-parameter-with-explicit-methods.md)
- **Similar refactorings:** [Extract Method](extract-method.md)
- **Similar refactorings:** [Form Template Method](form-template-method.md)
