# Separate Query from Modifier

**Category:** Simplifying Method Calls  

## Problem

One method both returns information and changes observable state.

## Refactoring

Split it into a side-effect-free query and a command.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Preserve ordering and atomicity when callers previously relied on the combined operation. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify the returned value and every side effect.
3. Create a query that computes the value without mutation.
4. Keep mutation in a command and update callers to invoke the required operations explicitly.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Helps other refactorings:** [Replace Temp with Query](replace-temp-with-query.md)
