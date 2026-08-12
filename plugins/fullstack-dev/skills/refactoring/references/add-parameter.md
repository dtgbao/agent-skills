# Add Parameter

**Category:** Simplifying Method Calls  

## Problem

A method needs information that its current interface cannot obtain appropriately.

## Refactoring

Add an explicit parameter and supply it from callers.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Do not add a parameter when the method should own the lookup or when it creates avoidable coupling. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Define the parameter's meaning and valid values.
3. Update the method and all overrides.
4. Migrate callers with correct data, using a temporary default only when compatibility requires it.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Remove Parameter](remove-parameter.md)
- **Similar refactorings:** [Rename Method](rename-method.md)
- **Helps other refactorings:** [Introduce Parameter Object](introduce-parameter-object.md)
