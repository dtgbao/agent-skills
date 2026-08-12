# Change Unidirectional Association to Bidirectional

**Category:** Organizing Data  

## Problem

Two objects need to navigate their relationship, but only one side currently stores it.

## Refactoring

Add a back-reference and centralize link updates so both sides remain consistent.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Bidirectional links increase coupling and can create ownership, serialization, and recursion problems. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Choose one method as the authority for creating and removing links.
3. Add the reverse reference.
4. Update both sides atomically and migrate callers to the link methods.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Change Bidirectional Association to Unidirectional](change-bidirectional-association-to-unidirectional.md)
