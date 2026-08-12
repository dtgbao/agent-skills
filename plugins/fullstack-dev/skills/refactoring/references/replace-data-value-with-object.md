# Replace Data Value with Object

**Category:** Organizing Data  

## Problem

A primitive value carries domain meaning or behavior that is scattered around its users.

## Refactoring

Introduce a small value object and move the associated rules into it.

## Why use it

Give data explicit meaning, ownership, and mutation rules. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Define equality, formatting, parsing, persistence, and nullability before replacing a widely used primitive. Preserve identity, equality, mutability, persistence, and serialization semantics.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Create a value type that initially wraps the primitive.
3. Migrate construction and access without changing behavior.
4. Move related validation and behavior into the value type incrementally.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Extract Class](extract-class.md)
- **Similar refactorings:** [Introduce Parameter Object](introduce-parameter-object.md)
- **Similar refactorings:** [Replace Array with Object](replace-array-with-object.md)
- **Similar refactorings:** [Replace Method with Method Object](replace-method-with-method-object.md)
