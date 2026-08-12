# Remove Parameter

**Category:** Simplifying Method Calls  

## Problem

A parameter is unused or no longer affects the method's contract.

## Refactoring

Remove it from the method and all callers.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Check overrides, callbacks, reflection, framework conventions, and binary compatibility before changing the signature. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Prove the parameter has no behavioral role.
3. Update declarations and call sites.
4. Remove derived values and tests that existed solely to supply it.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Add Parameter](add-parameter.md)
- **Similar refactorings:** [Rename Method](rename-method.md)
- **Helps other refactorings:** [Replace Parameter with Method Call](replace-parameter-with-method-call.md)
