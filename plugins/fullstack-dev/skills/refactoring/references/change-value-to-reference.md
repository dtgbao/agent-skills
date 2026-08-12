# Change Value to Reference

**Category:** Organizing Data  

## Problem

Multiple equal value objects actually represent one shared domain entity.

## Refactoring

Reuse a canonical reference so all users address the same entity instance.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Identity introduces lifecycle, lookup, caching, and mutation concerns that values do not have. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Define the stable identity key.
3. Introduce a repository, registry, or other canonical lookup.
4. Replace independent construction and verify shared updates deliberately.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Change Reference to Value](change-reference-to-value.md)
