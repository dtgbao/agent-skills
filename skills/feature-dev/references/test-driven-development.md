# Planning Test-Driven Development

Plan every behavior as a paired RED leaf followed by a dependent GREEN leaf. Production behavior follows a test that failed for the expected reason.

## Contents

- [The Pair Contract](#the-pair-contract)
- [RED Evidence](#red-evidence)
- [GREEN and Refactor Evidence](#green-and-refactor-evidence)
- [Exceptions](#exceptions)
- [Review](#review)

## The Pair Contract

Keep tests and implementation as separate adjacent subtasks so each stays short while their dependency preserves test-first order:

1. The RED leaf writes one focused behavioral test and observes the expected failure.
2. The GREEN leaf depends directly on RED, implements the minimum behavior, proves focused and related tests pass, and refactors while green.

Use the same requirement or bugfix identifiers on both leaves. Begin another pair for another independently observable behavior.

## RED Evidence

Name the test path, setup, public interface, behavior, and assertion. Record the exact focused command and expected failure. Confirm the test fails rather than errors and that the failure comes from missing behavior rather than a typo, fixture, or environment problem.

When a test passes immediately, identify existing behavior or strengthen the assertion before moving to GREEN. When it errors, repair the test environment until the intended behavioral assertion fails.

Prefer real behavior over mock interactions. Read [testing anti-patterns](testing-anti-patterns.md) when the design introduces mocks, test utilities, or production seams used only by tests.

## GREEN and Refactor Evidence

Name the smallest paths and symbols that implement the approved `design.md` contract. Do not restate the contract or add unapproved behavior. Record the focused command plus the smallest relevant regression command and their expected successful results.

Refactor only after GREEN. Remove duplication, improve names, or extract focused helpers while preserving the public contract, then rerun the stated evidence. State an explicit no-cleanup decision when the minimal implementation is already clear.

## Exceptions

Use `[TDD Exception]` only after explicit user approval for throwaway exploration, generated output, configuration-only work, or another case where behavioral RED cannot apply. Record Reason, Approval, and an exact Check with expected evidence.

Optional behavior is not an exception. Plan its own optional RED/GREEN pair.

## Review

Confirm every behavior has one adjacent pair, every implementation depends on its RED leaf, both leaves trace the same upstream identifiers, every command states expected evidence, and no production behavior appears before verified RED.
