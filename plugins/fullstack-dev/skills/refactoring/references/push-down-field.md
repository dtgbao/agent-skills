# Push Down Field

**Category:** Dealing with Generalization  

## Problem

A superclass stores data used by only certain subclasses.

## Refactoring

Move the field to the subtype that owns the state.

## Why use it

Align abstractions and hierarchies with behavior that is actually shared or specialized. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Check serialized layouts, constructors, protected access, and queries through the base type. Preserve substitutability, construction order, dispatch behavior, and public type relationships.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify the true owner and every access.
3. Add and initialize the field on that subtype.
4. Redirect uses and remove the superclass field.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Pull Up Field](pull-up-field.md)
- **Similar refactorings:** [Push Down Method](push-down-method.md)
- **Helps other refactorings:** [Extract Subclass](extract-subclass.md)
