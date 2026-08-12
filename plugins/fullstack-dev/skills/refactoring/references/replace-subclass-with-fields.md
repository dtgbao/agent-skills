# Replace Subclass with Fields

**Category:** Organizing Data  

## Problem

Subclasses differ only by fixed data and add no distinct behavior.

## Refactoring

Represent those differences as fields on the base class and remove the trivial subclasses.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Ensure the field combinations cannot represent invalid variants and preserve construction semantics. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Add fields for the fixed differences.
3. Provide factories or constructors for valid combinations.
4. Migrate instances and remove subclasses once type-specific behavior is gone.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md)
