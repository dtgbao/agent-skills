# Change Reference to Value

**Category:** Organizing Data  

## Problem

A shared reference has no meaningful identity and makes ownership or mutation unnecessarily complex.

## Refactoring

Make the object an immutable value that can be copied and compared by content.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Do not remove identity when callers depend on shared mutation, lifecycle, or reference equality. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Confirm all meaningful state participates in value equality.
3. Remove mutators and make construction complete.
4. Replace identity-based lookup and comparison with value semantics.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Change Value to Reference](change-value-to-reference.md)
