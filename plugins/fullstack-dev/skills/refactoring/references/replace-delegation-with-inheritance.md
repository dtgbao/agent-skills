# Replace Delegation with Inheritance

**Category:** Dealing with Generalization  

## Problem

A wrapper forwards nearly the entire interface of one stable collaborator and is genuinely substitutable for it.

## Refactoring

Inherit from the collaborator type and remove redundant forwarding methods.

## Why use it

Align abstractions and hierarchies with behavior that is actually shared or specialized. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Use this only for a real is-a relationship; inheritance exposes superclass evolution and forbids other class inheritance. Preserve substitutability, construction order, dispatch behavior, and public type relationships.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Verify the wrapper satisfies the collaborator's full contract.
3. Introduce the inheritance relationship.
4. Remove forwarding methods and the delegate field incrementally while preserving overrides.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Replace Inheritance with Delegation](replace-inheritance-with-delegation.md)
- **Similar refactorings:** [Remove Middle Man](remove-middle-man.md)
