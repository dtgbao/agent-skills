# Preserve Whole Object

**Category:** Simplifying Method Calls  

## Problem

A caller extracts several values from one object only to pass them separately.

## Refactoring

Pass the source object and let the callee read the values it needs.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

The shorter signature may introduce a dependency on a broad object; prefer a smaller value object when that coupling is undesirable. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Confirm the values share one source object.
3. Add the object parameter and read required values inside the method.
4. Migrate callers, then remove redundant scalar parameters.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Introduce Parameter Object](introduce-parameter-object.md)
- **Similar refactorings:** [Replace Parameter with Method Call](replace-parameter-with-method-call.md)
