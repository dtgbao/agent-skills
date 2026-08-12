# Replace Type Code with Subclasses

**Category:** Organizing Data  

## Problem

A stable type code controls behavior that varies by kind.

## Refactoring

Represent each kind with a subclass and dispatch behavior through the shared abstraction.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Avoid this when the kind changes during an object's lifetime or when only data, not behavior, varies. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Encapsulate construction of the coded type.
3. Introduce one subclass per behaviorally distinct code.
4. Move conditional behavior into overrides and remove the code after migration.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Replace Subclass with Fields](replace-subclass-with-fields.md)
- **Similar refactorings:** [Replace Type Code with Class](replace-type-code-with-class.md)
- **Similar refactorings:** [Replace Type Code with State/Strategy](replace-type-code-with-state-strategy.md)
