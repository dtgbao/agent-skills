# Replace Type Code with State/Strategy

**Category:** Organizing Data  

## Problem

A changeable type code or constrained hierarchy selects among distinct behaviors.

## Refactoring

Store a state or strategy object and delegate the varying behavior to it.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Make state transitions explicit and avoid a class hierarchy when a small function or table is sufficient. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Define the behavior contract selected by the code.
3. Create implementations for the meaningful variants.
4. Delegate behavior, migrate transitions, and remove code-based branching.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Replace Type Code with Class](replace-type-code-with-class.md)
- **Similar refactorings:** [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md)
