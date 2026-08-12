# Extract Class

**Category:** Moving Features between Objects  

## Problem

One class carries responsibilities that change for different reasons.

## Refactoring

Create a focused class and move one cohesive responsibility into it.

## Why use it

Put behavior and data with the object that owns the relevant responsibility. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

A split that creates constant back-and-forth calls or duplicated state may reduce cohesion rather than improve it. Check visibility, dependency direction, object ownership, and every existing caller.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify a cohesive cluster of fields and behavior.
3. Create the new class and establish one clear relationship to it.
4. Move members incrementally and narrow the original class interface.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Inline Class](inline-class.md)
- **Similar refactorings:** [Extract Subclass](extract-subclass.md)
- **Similar refactorings:** [Replace Data Value with Object](replace-data-value-with-object.md)
