# Introduce Foreign Method

**Category:** Moving Features between Objects  

## Problem

A third-party or otherwise closed type lacks one small operation needed by a client.

## Refactoring

Create a clearly marked helper near the client and pass the foreign object to it.

## Why use it

Put behavior and data with the object that owns the relevant responsibility. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Use this for isolated gaps; multiple related additions call for a local extension instead. Check visibility, dependency direction, object ownership, and every existing caller.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Define the missing operation in the client context.
3. Accept or obtain the foreign object explicitly.
4. Replace duplicated client-side fragments and document why the helper is external to the type.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Introduce Local Extension](introduce-local-extension.md)
