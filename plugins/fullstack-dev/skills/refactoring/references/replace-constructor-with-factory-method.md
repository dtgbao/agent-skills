# Replace Constructor with Factory Method

**Category:** Simplifying Method Calls  

## Problem

Direct construction cannot express variant selection, naming, caching, or other creation policy clearly.

## Refactoring

Expose a factory method and route construction through it.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Factories can hide allocation and dependencies; keep creation policy explicit and avoid needless indirection. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Create a factory that initially delegates to the constructor.
3. Give it a name that describes the created variant or policy.
4. Migrate callers, then restrict the constructor only when required.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Helps other refactorings:** [Change Value to Reference](change-value-to-reference.md)
- **Helps other refactorings:** [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md)
