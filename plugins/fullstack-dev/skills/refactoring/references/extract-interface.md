# Extract Interface

**Category:** Dealing with Generalization  

## Problem

Several classes expose a common capability that clients should depend on without sharing implementation.

## Refactoring

Define an interface for that client-facing capability and have the classes implement it.

## Why use it

Align abstractions and hierarchies with behavior that is actually shared or specialized. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Keep the interface cohesive and driven by client needs rather than mirroring every public method. Preserve substitutability, construction order, dispatch behavior, and public type relationships.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify the operations one client role actually requires.
3. Declare the minimal interface.
4. Adopt it in implementations and change consumers to depend on it.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Extract Superclass](extract-superclass.md)
