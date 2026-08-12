# Pull Up Constructor Body

**Category:** Dealing with Generalization  

## Problem

Subclass constructors repeat the same initialization work.

## Refactoring

Move the common initialization into the superclass constructor or a shared initialization operation.

## Why use it

Align abstractions and hierarchies with behavior that is actually shared or specialized. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Constructor order, partially initialized objects, and virtual dispatch can make this refactoring unsafe. Preserve substitutability, construction order, dispatch behavior, and public type relationships.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify statements that are identical and independent of subclass state.
3. Move them to the superclass initialization path.
4. Pass required values explicitly and verify construction order.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Pull Up Method](pull-up-method.md)
