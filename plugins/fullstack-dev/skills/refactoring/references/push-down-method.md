# Push Down Method

**Category:** Dealing with Generalization  

## Problem

A superclass method is meaningful for only a subset of subclasses.

## Refactoring

Move the method to the subclass or intermediate subtype that actually supports it.

## Why use it

Align abstractions and hierarchies with behavior that is actually shared or specialized. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Callers typed as the superclass may reveal that the original abstraction promised too much. Preserve substitutability, construction order, dispatch behavior, and public type relationships.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Find all callers and supported runtime types.
3. Move or copy the method to the appropriate subtype.
4. Update contracts and remove the superclass method after unsupported calls are eliminated.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Pull Up Method](pull-up-method.md)
- **Similar refactorings:** [Push Down Field](push-down-field.md)
- **Helps other refactorings:** [Extract Subclass](extract-subclass.md)
