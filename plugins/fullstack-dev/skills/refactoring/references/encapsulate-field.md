# Encapsulate Field

**Category:** Organizing Data  

## Problem

External code reads or writes a public field directly.

## Refactoring

Make the field non-public and expose intentional access operations.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Accessors are an interface commitment; expose behavior instead when raw state should not be public. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Introduce read or write operations only for supported use cases.
3. Migrate external access.
4. Restrict the field after all callers use the new interface.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Self Encapsulate Field](self-encapsulate-field.md)
