# Inline Class

**Category:** Moving Features between Objects  

## Problem

A class no longer has enough independent responsibility to justify its boundary.

## Refactoring

Move its behavior and data into the most appropriate consumer, then remove the class.

## Why use it

Put behavior and data with the object that owns the relevant responsibility. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Keep the class when its name captures a useful domain concept or preserves a valuable seam. Check visibility, dependency direction, object ownership, and every existing caller.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Select the recipient that already owns the surrounding responsibility.
3. Move public behavior and state while redirecting callers.
4. Remove forwarding code and delete the class after references disappear.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Extract Class](extract-class.md)
