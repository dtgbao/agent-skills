# Collapse Hierarchy

**Category:** Dealing with Generalization  

## Problem

A superclass and subclass no longer differ enough to justify separate types.

## Refactoring

Merge them into the type that best represents the remaining responsibility.

## Why use it

Align abstractions and hierarchies with behavior that is actually shared or specialized. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Preserve public type names, discriminators, persistence, and construction compatibility during migration. Preserve substitutability, construction order, dispatch behavior, and public type relationships.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Choose the surviving type and confirm substitutability.
3. Move fields and methods into it.
4. Migrate references and constructors, then remove the empty hierarchy level.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Inline Class](inline-class.md)
