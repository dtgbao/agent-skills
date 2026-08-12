# Pull Up Field

**Category:** Dealing with Generalization  

## Problem

Sibling subclasses declare equivalent fields that represent the same concept.

## Refactoring

Move one field declaration to their common superclass.

## Why use it

Align abstractions and hierarchies with behavior that is actually shared or specialized. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Confirm type, visibility, initialization, persistence, and meaning are truly equivalent. Preserve substitutability, construction order, dispatch behavior, and public type relationships.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Compare the duplicate fields and their uses.
3. Declare the shared field on the superclass.
4. Redirect initialization and remove subclass declarations one at a time.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Push Down Field](push-down-field.md)
- **Similar refactorings:** [Pull Up Method](pull-up-method.md)
