# Extract Superclass

**Category:** Dealing with Generalization  

## Problem

Several classes independently implement the same state or behavior.

## Refactoring

Create a superclass for the genuine common abstraction and move shared members into it.

## Why use it

Align abstractions and hierarchies with behavior that is actually shared or specialized. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Do not force unrelated classes into inheritance solely to reuse code; delegation may express the relationship better. Preserve substitutability, construction order, dispatch behavior, and public type relationships.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify the shared contract and invariant.
3. Create the superclass with the smallest useful interface.
4. Pull up common fields and methods incrementally, then update construction.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Extract Interface](extract-interface.md)
