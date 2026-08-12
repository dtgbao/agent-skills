# Move Field

**Category:** Moving Features between Objects  

## Problem

A field is stored on an object that does not primarily own or use the value.

## Refactoring

Move the field and its access responsibility to the appropriate object.

## Why use it

Put behavior and data with the object that owns the relevant responsibility. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Check persistence mappings, serialization, equality, initialization, and shared ownership before moving state. Check visibility, dependency direction, object ownership, and every existing caller.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Choose the owner based on invariants and usage.
3. Add storage and access on the recipient.
4. Redirect reads and writes, migrate initialization, then remove the old field.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Move Method](move-method.md)
- **Helps other refactorings:** [Extract Class](extract-class.md)
- **Helps other refactorings:** [Inline Class](inline-class.md)
