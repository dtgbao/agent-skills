# Self Encapsulate Field

**Category:** Organizing Data  

## Problem

A class accesses its own field directly, making future access policy difficult to centralize.

## Refactoring

Route internal reads and writes through access methods.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Avoid accidental recursion and account for construction paths that run before the object is fully initialized. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Create internal read and write methods with the current semantics.
3. Replace direct access inside the class.
4. Add validation or indirection only after the access path is stable.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Encapsulate Field](encapsulate-field.md)
- **Helps other refactorings:** [Duplicate Observed Data](duplicate-observed-data.md)
- **Helps other refactorings:** [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md)
- **Helps other refactorings:** [Replace Type Code with State/Strategy](replace-type-code-with-state-strategy.md)
