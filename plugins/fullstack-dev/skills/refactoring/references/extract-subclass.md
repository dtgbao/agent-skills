# Extract Subclass

**Category:** Dealing with Generalization  

## Problem

A class contains optional or variant behavior needed only by some instances.

## Refactoring

Create a subclass for the distinct responsibility and move the relevant state and behavior into it.

## Why use it

Align abstractions and hierarchies with behavior that is actually shared or specialized. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Prefer composition when variants change at runtime or when subclassing would violate substitutability. Preserve substitutability, construction order, dispatch behavior, and public type relationships.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Define the behavioral distinction and how instances are created.
3. Create the subclass and move one feature cluster into it.
4. Migrate construction and remove type checks made unnecessary by dispatch.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Extract Class](extract-class.md)
