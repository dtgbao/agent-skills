# Form Template Method

**Category:** Dealing with Generalization  

## Problem

Related subclasses implement the same algorithm shape with duplicated sequencing.

## Refactoring

Move the shared sequence into a template method and leave variation in overridable steps.

## Why use it

Align abstractions and hierarchies with behavior that is actually shared or specialized. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Template methods couple variation to inheritance; prefer composition when steps must vary independently at runtime. Preserve substitutability, construction order, dispatch behavior, and public type relationships.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Compare algorithms and align equivalent steps.
3. Extract differing steps behind common method names.
4. Pull the shared sequence into the superclass and verify every subtype order.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
