# Duplicate Observed Data

**Category:** Organizing Data  

## Problem

Presentation state and domain state are coupled even though they have different responsibilities.

## Refactoring

Keep domain data in a domain object and synchronize the presentation copy through explicit observation.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Prevent feedback loops, stale copies, and ambiguous ownership of updates. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Create the domain representation and copy the current value into it.
3. Define one direction for each update and a synchronization mechanism.
4. Move domain behavior off the presentation object and test both update paths.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
