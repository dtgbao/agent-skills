# Replace Type Code with Class

**Category:** Organizing Data  

## Problem

A primitive type code represents a domain category and is passed around without type safety.

## Refactoring

Wrap the code in a dedicated class or value type.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

This is most useful when the category has meaning but does not yet require polymorphic behavior. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Create a type that represents the valid codes.
3. Migrate fields, parameters, and comparisons.
4. Centralize parsing and validation, then remove primitive constants from domain code.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md)
- **Similar refactorings:** [Replace Type Code with State/Strategy](replace-type-code-with-state-strategy.md)
