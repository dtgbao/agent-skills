# Rename Method

**Category:** Simplifying Method Calls  

## Problem

A method name no longer states its purpose accurately.

## Refactoring

Choose a name that communicates intent and update every caller.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

For public interfaces, use a compatibility shim or planned migration instead of an abrupt rename. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Derive the new name from the method's responsibility and result.
3. Update declarations, overrides, references, tests, and documentation.
4. Remove any temporary alias after consumers migrate.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Add Parameter](add-parameter.md)
- **Similar refactorings:** [Remove Parameter](remove-parameter.md)
