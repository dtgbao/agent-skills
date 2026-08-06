---
name: design-pattern
description: TypeScript implementations of the 22 Gang of Four design patterns. Use when writing, reviewing, or refactoring object-oriented TypeScript code that needs creational, structural, or behavioral patterns, or when comparing closely related patterns and their tradeoffs.
---

# TypeScript Design Patterns

Comprehensive catalog of 22 Gang of Four patterns across 3 categories. Each rule explains applicability, tradeoffs, an incorrect approach, and a correct TypeScript implementation.

## When to Apply

Reference these guidelines when:

- Selecting a pattern for an existing design problem
- Replacing rigid conditionals or tightly coupled object creation
- Integrating incompatible interfaces or composing object structures
- Encapsulating algorithms, workflows, state transitions, or notifications
- Reviewing whether a pattern is correctly implemented
- Comparing patterns with similar structures but different intent

## Pattern Categories

| Category   | Purpose                                    | Prefix      |
| ---------- | ------------------------------------------ | ----------- |
| Creational | Control how objects are created            | `create-`   |
| Structural | Compose classes and objects                | `struct-`   |
| Behavioral | Coordinate responsibilities and algorithms | `behavior-` |

## Quick Reference

| Impact   | Rule                               | Category   | Description                                             |
| -------- | ---------------------------------- | ---------- | ------------------------------------------------------- |
| CRITICAL | `create-abstract-factory`          | Creational | Create compatible families of related products          |
| CRITICAL | `create-builder`                   | Creational | Construct complex objects step by step                  |
| CRITICAL | `create-factory-method`            | Creational | Delegate product creation through a common contract     |
| CRITICAL | `struct-adapter`                   | Structural | Translate an incompatible interface                     |
| CRITICAL | `behavior-command`                 | Behavioral | Represent a request as an object                        |
| CRITICAL | `behavior-iterator`                | Behavioral | Traverse a collection without exposing representation   |
| CRITICAL | `behavior-observer`                | Behavioral | Notify dynamic subscribers of changes                   |
| CRITICAL | `behavior-strategy`                | Behavioral | Swap interchangeable algorithms                         |
| HIGH     | `create-prototype`                 | Creational | Copy configured objects without concrete-class coupling |
| HIGH     | `create-singleton`                 | Creational | Restrict a class to one globally accessible instance    |
| HIGH     | `struct-composite`                 | Structural | Treat leaves and containers uniformly                   |
| HIGH     | `struct-decorator`                 | Structural | Stack behavior around an object                         |
| HIGH     | `struct-facade`                    | Structural | Provide a simplified subsystem interface                |
| HIGH     | `behavior-chain-of-responsibility` | Behavioral | Pass requests through ordered handlers                  |
| HIGH     | `behavior-state`                   | Behavioral | Change behavior with internal state                     |
| HIGH     | `behavior-template-method`         | Behavioral | Fix an algorithm skeleton while varying steps           |
| MEDIUM   | `struct-bridge`                    | Structural | Separate independently varying dimensions               |
| MEDIUM   | `struct-proxy`                     | Structural | Control access through a substitutable stand-in         |
| MEDIUM   | `behavior-memento`                 | Behavioral | Snapshot and restore encapsulated state                 |
| MEDIUM   | `behavior-visitor`                 | Behavioral | Add operations to a stable object hierarchy             |
| LOW      | `struct-flyweight`                 | Structural | Share immutable state across many objects               |
| LOW      | `behavior-mediator`                | Behavioral | Centralize collaboration between components             |

## How to Use

Read the individual rule that matches the design pressure:

```text
rules/create-builder.md
rules/struct-adapter.md
rules/behavior-strategy.md
rules/_sections.md
```

Each rule contains:

- Intent and applicability signals
- An incorrect approach and why it fails
- A correct TypeScript implementation
- Tradeoffs and related-pattern distinctions
- Links to the main article and TypeScript code example

Prefer the simplest solution that works. Do not add a pattern for a hypothetical variation or merely to match a familiar class diagram.
