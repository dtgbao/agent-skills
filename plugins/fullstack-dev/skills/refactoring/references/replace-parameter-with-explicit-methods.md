# Replace Parameter with Explicit Methods

**Category:** Simplifying Method Calls  

## Problem

A parameter selects between distinct behaviors, making calls difficult to read.

## Refactoring

Provide a named method for each supported behavior and remove the selector parameter.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Avoid an oversized interface when variants are numerous or data-driven. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Enumerate the stable selector values and their behaviors.
3. Create an intention-revealing method for each case.
4. Move callers and remove the parameterized dispatcher when unused.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Parameterize Method](parameterize-method.md)
- **Similar refactorings:** [Replace Conditional with Polymorphism](replace-conditional-with-polymorphism.md)
