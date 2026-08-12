# Replace Inheritance with Delegation

**Category:** Dealing with Generalization  

## Problem

A subclass is not truly substitutable for its superclass or uses only a small part of it.

## Refactoring

Hold a collaborator instance and delegate the required operations instead of inheriting.

## Why use it

Align abstractions and hierarchies with behavior that is actually shared or specialized. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Account for protected members, identity, lifecycle, and clients that currently rely on the subtype relationship. Preserve substitutability, construction order, dispatch behavior, and public type relationships.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Add a field for the delegated object.
3. Create explicit forwarding operations for the supported behavior.
4. Migrate inherited usage, remove the extends relationship, and construct the delegate directly.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Replace Delegation with Inheritance](replace-delegation-with-inheritance.md)
