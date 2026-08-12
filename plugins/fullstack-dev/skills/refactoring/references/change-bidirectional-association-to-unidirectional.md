# Change Bidirectional Association to Unidirectional

**Category:** Organizing Data  

## Problem

One side of a two-way relationship is unused or can be obtained another way.

## Refactoring

Remove the unnecessary back-reference and maintain the association from one owner.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Confirm no invariant, persistence mapping, or traversal depends on the removed direction. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Find all reads and writes of the removable direction.
3. Provide an alternative query only where genuinely needed.
4. Remove synchronization code and the back-reference together.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Change Unidirectional Association to Bidirectional](change-unidirectional-association-to-bidirectional.md)
