# Pull Up Method

**Category:** Dealing with Generalization  

## Problem

Sibling subclasses contain equivalent implementations of the same operation.

## Refactoring

Move the common implementation to their superclass.

## Why use it

Align abstractions and hierarchies with behavior that is actually shared or specialized. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Differences hidden in helper calls, state, or side effects can make superficially similar methods non-equivalent. Preserve substitutability, construction order, dispatch behavior, and public type relationships.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Prove the implementations and required contracts are compatible.
3. Align signatures and move required shared members first.
4. Move the method to the superclass and delete duplicates.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Push Down Method](push-down-method.md)
- **Similar refactorings:** [Pull Up Field](pull-up-field.md)
- **Helps other refactorings:** [Form Template Method](form-template-method.md)
