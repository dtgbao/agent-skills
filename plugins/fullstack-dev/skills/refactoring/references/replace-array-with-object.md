# Replace Array with Object

**Category:** Organizing Data  

## Problem

Array positions encode different fields, forcing callers to remember index meanings.

## Refactoring

Replace the positional structure with a named object or record.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Preserve ordering and wire-format requirements at adapters rather than leaking positions into domain code. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Create a type with a named field for every meaningful position.
3. Migrate reads and writes one index at a time.
4. Convert at external boundaries, then remove positional access internally.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Replace Data Value with Object](replace-data-value-with-object.md)
