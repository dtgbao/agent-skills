# Replace Magic Number with Symbolic Constant

**Category:** Organizing Data  

## Problem

A literal value appears in code without communicating its domain meaning.

## Refactoring

Give the value a named constant and replace uses that share that meaning.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Do not merge identical literals that represent different units, policies, or concepts. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify the concept and choose a precise name.
3. Declare the constant at the narrowest shared scope.
4. Replace semantically equivalent occurrences and verify unit consistency.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
