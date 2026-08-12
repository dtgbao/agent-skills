---
name: refactoring
description: Behavior-preserving refactoring workflow with a catalog of 23 code smells and 66 language-neutral techniques. Use when diagnosing maintainability problems, selecting a named refactoring, restructuring existing code without changing observable behavior, planning incremental technical-debt cleanup, or reviewing refactoring safety.
---

# Refactoring

Improve the internal design of existing code without adding features or changing observable behavior. Refactor in small, reversible steps and keep the program working after every step.

## Use bundled knowledge

Treat this skill and its `references/` files as the complete working catalog. Do not browse
Refactoring.Guru during normal use; external reading defeats the purpose of the bundled references
and wastes context. Open an external source only when the user explicitly asks to verify or update
the catalog, or when a required technique is demonstrably missing from the bundled material.

Load progressively: read the checklist to identify a smell, then read only the selected local
technique files. Do not load all 66 techniques for one task.

## What is refactoring?

Refactoring changes structure, names, responsibilities, dependencies, or interfaces while preserving the behavior that callers and users rely on. It is not a rewrite, a feature change, or an excuse to redesign unrelated code. Establish the behavioral boundary before editing: inputs, outputs, side effects, error behavior, ordering, performance constraints, and compatibility obligations may all be part of the contract.

### Clean code

Prefer code whose intent is apparent to another maintainer, avoids needless duplication and moving parts, passes its tests, and is economical to change. “Clean” is contextual: follow the repository's conventions and improve the concrete pressure in front of you rather than optimizing for line count or personal style.

### Technical debt

Treat technical debt as the future change cost created by today's expedient decisions. Typical causes include delivery pressure, weak feedback from tests, tightly coupled components, missing shared knowledge or documentation, long-lived branches, delayed cleanup, inconsistent engineering practices, and gaps in experience. Refactor when paying down a demonstrated debt reduces current delivery or reliability risk; do not create speculative abstractions.

### When to refactor

Refactor when repeated code or structure has become a real pattern, before adding a feature to a resistant area, while localizing the cause of a defect, or during review when the change is still fresh. Use the rule of three as a restraint: tolerate the first occurrence, notice the second, and generalize only when the third confirms the pattern. Avoid unrelated cleanup that obscures the requested change.

### How to refactor

Make one behavior-preserving transformation at a time. Keep feature development and refactoring in separate changes or commits. Existing tests must continue to pass; when tests are coupled to private implementation, replace them with tests of observable behavior before restructuring. Consider a rewrite only when incremental improvement cannot produce a maintainable result and a separately approved, well-tested migration is available.

## Workflow

1. Read repository instructions and neighboring code. State the behavior and scope that must not change.
2. Run existing focused tests. If coverage is insufficient, add or identify characterization checks before restructuring.
3. Read [the code smell checklist](references/code-smell-checklist.md). Confirm the smell from evidence; a checklist match is a prompt to investigate, not an automatic verdict.
4. Select the least invasive treatment and read its technique file below. Prefer a repository-native helper or simpler language/platform feature when it solves the pressure.
5. Apply one technique step at a time. Run focused checks after each stable step and keep the diff limited to the requested area.
6. Run the broader relevant suite, compare observable behavior, inspect the final diff, and document any intentional interface migration separately.

Stop if the required change alters behavior, expands scope materially, lacks a verification path, or conflicts with a public compatibility obligation. Reclassify the work as a feature, bug fix, migration, or redesign and obtain the appropriate approval.

## Technique catalog

Read only the technique relevant to the confirmed pressure. Each reference summarizes the problem, transformation, motivation, cautions, incremental procedure, and related local techniques.

### Composing Methods (9)

- [Extract Method](references/extract-method.md)
- [Inline Method](references/inline-method.md)
- [Extract Variable](references/extract-variable.md)
- [Inline Temp](references/inline-temp.md)
- [Replace Temp with Query](references/replace-temp-with-query.md)
- [Split Temporary Variable](references/split-temporary-variable.md)
- [Remove Assignments to Parameters](references/remove-assignments-to-parameters.md)
- [Replace Method with Method Object](references/replace-method-with-method-object.md)
- [Substitute Algorithm](references/substitute-algorithm.md)

### Moving Features between Objects (8)

- [Move Method](references/move-method.md)
- [Move Field](references/move-field.md)
- [Extract Class](references/extract-class.md)
- [Inline Class](references/inline-class.md)
- [Hide Delegate](references/hide-delegate.md)
- [Remove Middle Man](references/remove-middle-man.md)
- [Introduce Foreign Method](references/introduce-foreign-method.md)
- [Introduce Local Extension](references/introduce-local-extension.md)

### Organizing Data (15)

- [Self Encapsulate Field](references/self-encapsulate-field.md)
- [Replace Data Value with Object](references/replace-data-value-with-object.md)
- [Change Value to Reference](references/change-value-to-reference.md)
- [Change Reference to Value](references/change-reference-to-value.md)
- [Replace Array with Object](references/replace-array-with-object.md)
- [Duplicate Observed Data](references/duplicate-observed-data.md)
- [Change Unidirectional Association to Bidirectional](references/change-unidirectional-association-to-bidirectional.md)
- [Change Bidirectional Association to Unidirectional](references/change-bidirectional-association-to-unidirectional.md)
- [Replace Magic Number with Symbolic Constant](references/replace-magic-number-with-symbolic-constant.md)
- [Encapsulate Field](references/encapsulate-field.md)
- [Encapsulate Collection](references/encapsulate-collection.md)
- [Replace Type Code with Class](references/replace-type-code-with-class.md)
- [Replace Type Code with Subclasses](references/replace-type-code-with-subclasses.md)
- [Replace Type Code with State/Strategy](references/replace-type-code-with-state-strategy.md)
- [Replace Subclass with Fields](references/replace-subclass-with-fields.md)

### Simplifying Conditional Expressions (8)

- [Decompose Conditional](references/decompose-conditional.md)
- [Consolidate Conditional Expression](references/consolidate-conditional-expression.md)
- [Consolidate Duplicate Conditional Fragments](references/consolidate-duplicate-conditional-fragments.md)
- [Remove Control Flag](references/remove-control-flag.md)
- [Replace Nested Conditional with Guard Clauses](references/replace-nested-conditional-with-guard-clauses.md)
- [Replace Conditional with Polymorphism](references/replace-conditional-with-polymorphism.md)
- [Introduce Null Object](references/introduce-null-object.md)
- [Introduce Assertion](references/introduce-assertion.md)

### Simplifying Method Calls (14)

- [Rename Method](references/rename-method.md)
- [Add Parameter](references/add-parameter.md)
- [Remove Parameter](references/remove-parameter.md)
- [Separate Query from Modifier](references/separate-query-from-modifier.md)
- [Parameterize Method](references/parameterize-method.md)
- [Replace Parameter with Explicit Methods](references/replace-parameter-with-explicit-methods.md)
- [Preserve Whole Object](references/preserve-whole-object.md)
- [Replace Parameter with Method Call](references/replace-parameter-with-method-call.md)
- [Introduce Parameter Object](references/introduce-parameter-object.md)
- [Remove Setting Method](references/remove-setting-method.md)
- [Hide Method](references/hide-method.md)
- [Replace Constructor with Factory Method](references/replace-constructor-with-factory-method.md)
- [Replace Error Code with Exception](references/replace-error-code-with-exception.md)
- [Replace Exception with Test](references/replace-exception-with-test.md)

### Dealing with Generalization (12)

- [Pull Up Field](references/pull-up-field.md)
- [Pull Up Method](references/pull-up-method.md)
- [Pull Up Constructor Body](references/pull-up-constructor-body.md)
- [Push Down Method](references/push-down-method.md)
- [Push Down Field](references/push-down-field.md)
- [Extract Subclass](references/extract-subclass.md)
- [Extract Superclass](references/extract-superclass.md)
- [Extract Interface](references/extract-interface.md)
- [Collapse Hierarchy](references/collapse-hierarchy.md)
- [Form Template Method](references/form-template-method.md)
- [Replace Inheritance with Delegation](references/replace-inheritance-with-delegation.md)
- [Replace Delegation with Inheritance](references/replace-delegation-with-inheritance.md)

## Attribution

This bundled synthesis is based on the public
[Refactoring.Guru refactoring catalog](https://refactoring.guru/refactoring). This attribution link
is not required reading during normal skill use.
