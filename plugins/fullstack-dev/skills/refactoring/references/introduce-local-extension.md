# Introduce Local Extension

**Category:** Moving Features between Objects  

## Problem

A closed library type lacks several related operations needed throughout the codebase.

## Refactoring

Provide a local wrapper or safe subclass that adds the missing behavior.

## Why use it

Put behavior and data with the object that owns the relevant responsibility. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Choose wrapping when inheritance is unsafe, and define conversion, equality, and identity behavior explicitly. Check visibility, dependency direction, object ownership, and every existing caller.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Choose composition or inheritance based on the foreign type's contract.
3. Mirror only the required public surface and add the local operations.
4. Migrate consumers that need the extension without replacing unrelated uses.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Introduce Foreign Method](introduce-foreign-method.md)
