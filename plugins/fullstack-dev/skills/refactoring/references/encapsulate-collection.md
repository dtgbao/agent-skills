# Encapsulate Collection

**Category:** Organizing Data  

## Problem

Callers can replace or mutate an object's collection without preserving its invariants.

## Refactoring

Return a read-only view or copy and provide focused add/remove operations.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Preserve ordering, duplicate handling, ownership, and iteration behavior expected by callers. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Add focused mutation methods that enforce current rules.
3. Replace direct mutations with those methods.
4. Stop exposing the mutable collection and remove bulk replacement if unnecessary.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
