# Glossary

Each term has one meaning in all sdd files.

| Term | Meaning |
|---|---|
| baseline | The criterion text at design approval. `spec.py drift` compares the current text with it. |
| brief | One line: who needs what, why, how to see success, and one thing that is out of scope. |
| case | One TDD cycle with literal values, in a slice: `c1.1a: <setup>; <call>; -> <result>`. One test (it can be parametrized), red, then the code, green. |
| criterion | One numbered line in a requirement, with one `SHALL`. Its id is `N.M`. |
| drift | A change that a person made by hand to an approved section of `spec.md`. |
| frontier | The open decisions that you can ask about now, because all decisions before them are made. |
| gate | A stop where the user approves a section or asks for changes. Gate 1: requirements. Gate 2: design and plan. |
| keep case | A bugfix case for an Unchanged criterion. It must pass on the code before the fix. |
| lane | A chain of slices that one runner does in order. It owns its files; no other lane writes them. |
| lane-runner | The subagent that does one lane, one test at a time, as `spec.py tdd` tells it. |
| missing name | A test stops because a name does not exist (an import, name, attribute or call-signature error). It is not a red. Add a stub, then run again. |
| mutant | A copy of the code with one small change that breaks the behavior. A good test fails on it. |
| no-red | A case whose test passed on its first run. `spec.py` then tries simple mutants on the lane code. The case is done only when a mutant makes the test fail. |
| open question | A value that the input does not give. The writer gives a recommended answer; the user decides at gate 1. |
| playback | A short summary of what the user wants. The user must confirm it. |
| property | A rule that is true for all inputs in a range. A property test checks it with 100 or more generated inputs. |
| red, green | Red: the test reaches its assertion and fails, or an expected error is not raised. Green: the test passes. |
| seam | A public interface that a test calls. Tests do not call internal code. |
| slice | One behavior that a caller can see, with 1–3 criteria and their cases. |
| spec-writer | The subagent that writes and updates `spec.md`. |
| tier | The model of a lane: S = haiku, M = sonnet low, L = sonnet medium. A retry goes one step up, to sonnet high at most. |
| wave | A set of lanes that can run at the same time. |
