# Move Method

**Category:** Moving Features between Objects  

## Problem

A method relies more heavily on another object than on the object that currently declares it.

## Refactoring

Relocate the method to the object that owns most of the data or responsibility it uses.

## Why use it

Put behavior and data with the object that owns the relevant responsibility. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Moving behavior can expose internals or reverse a desirable dependency direction. Check visibility, dependency direction, object ownership, and every existing caller.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify the recipient and every dependency used by the method.
3. Create the method on the recipient and migrate its dependencies.
4. Delegate temporarily or update callers, then remove the old method when safe.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Extract Method](extract-method.md)
- **Similar refactorings:** [Move Field](move-field.md)
- **Helps other refactorings:** [Extract Class](extract-class.md)
- **Helps other refactorings:** [Inline Class](inline-class.md)
- **Helps other refactorings:** [Introduce Parameter Object](introduce-parameter-object.md)
