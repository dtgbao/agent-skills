# spec.md format

One file: `docs/specs/<name>/spec.md`. Three sections: Requirements (or Bug), Design, Plan. `spec.py` reads this format. Keep the exact line forms that this file shows.

```markdown
# Spec: <name>

Workflow: feature | bugfix
Test: `<command that runs one target>` — put `{target}` where the file or test goes
Suite: `<command that runs all tests and the typecheck>`

## Requirements

### R1: <title>
As <who>, I want <what>, so that <why>.

- 1.1 WHEN <trigger> THE <system> SHALL <response>.
- 1.2 IF <bad input or state> THEN THE <system> SHALL <rejection>.

### Out of scope
- <item>

### Open questions
- none

## Design

### Decisions
- <decision>: <reason>

### Interfaces
<code block in the project language: each new or changed public signature, with its file>

### Errors
| Cause | Result |
|---|---|

### Properties
- P1 (1.1, 1.3): For any <inputs and bounds>, <unit> SHALL <invariant>.

## Plan

### Lane A: <title>
Files: `<code file>`, `<test file>`
Tier: S | M | L
After: none | B

- [ ] A1 <behavior that a caller sees> · req 1.1, 1.2 · seam `<public interface>`
  - c1.1a: <given>; <call>; -> <expected>
  - c1.2a: <given>; <call>; -> raises <Error>
  - P1: property
```

## Requirements

- Write each criterion in EARS: `WHEN … THE … SHALL …`, `IF … THEN THE … SHALL …`, `WHILE …`, `WHERE …`. Each criterion has exactly one `SHALL` and one result that a test can see. Do not join two results with "and".
- Give each requirement 2–7 criteria. Give each input its limits (range, length, format) and the result for a value outside the limits.
- Write each value as a literal: `1–90`, `3999 cents`, `HTTP 409`. Do not write "valid", "fast" or "large".
- When the input does not say a value, do not guess. Add it to Open questions with your recommended answer: `- <question> (recommended: <answer>)`. The main session asks the user. After the answers, write the answers into the criteria and set Open questions to `- none`.
- Bugfix: use `## Bug` in place of `## Requirements`. Criteria `1.n` = Current (the wrong behavior now), `2.n` = Expected (the correct behavior), `3.n` = Unchanged (behavior that must stay the same). Cases cite `2.n` and `3.n`.

## Design

- Decisions: one line each, with the reason. Include each choice that a test can see: rounding, inclusive or exclusive limits, status codes, error types.
- Interfaces: the public signatures that tests call (the seams) and the signatures that change. Write them in the project language. These are the contract: a lane runner sees only this section, Errors, its criteria and its cases.
- Errors: one row for each failure that a caller can see.
- Properties: write a property for a rule that is true for all inputs in a range (an invariant, a round trip, a limit). Write the bounds and the oracle as literal values. Do not write a property for one fixed example.
- Read the code before you write the design. Use the names, the style and the test framework that the project uses. Take `Test:` and `Suite:` from the manifest scripts or the README. `Test:` must contain `{target}`.

## Plan

**Lanes.** A lane is a chain of slices that one runner does in order. It owns its `Files`, and no other lane writes them.

- Use the smallest number of lanes. Make a second lane only for work that touches other files and that can run at the same time.
- A lane that imports code from another lane names it in `After`.
- Each lane has one or more test files and one or more code files.
- `Tier`: S = simple cases with exact values; M = normal; L = a new algorithm, concurrency, security or money rounding.

**Slices.** A slice is one behavior that a caller can see. It goes through all the layers that it needs.

- A slice cites 1–3 criteria. Put the slices in the order that builds the behavior: the first slice is the shortest path through all the layers, with no limits and no error cases. The slices after it add one behavior each.
- The slice id starts with the lane id: `A1`, `A2`, `B1`.
- The seam is a public interface from Interfaces. Tests call only seams.

**Cases.** A case is one TDD cycle: one test that fails on the code before it, then the code that makes it pass. The runner does the cases one at a time, in order. Each cycle costs model calls, so write the fewest cases that drive all the code.

- Write each case with literal values: the setup, the call and the expected result. Example: `- c1.1a: cart TEA-01 x2 (450 each), code SAVE10 = 10%; cart.total_cents(); -> 810`.
- The case id is `c` + criterion id + a letter: `c1.1a`, `c1.1b`. A property case is `- P1: property`.
- Default: one case for each criterion. Add a second case only when it needs new code, for example the other side of a limit that the first case does not reach.
- Put more values of the same behavior in the same case, as examples: `- c1.5a: percent 0, 51; POST /codes; -> 400 for each`. The runner makes one parametrized test.
- Do not write a case that the earlier cases already make pass. If a value only confirms code that exists, add it as an example to the case that made that code.
- Each value must be possible through the seam with the code and data that exist then. Example: use prices that the catalog holds.
- Put the cases of a slice in this order: the normal case first, then the limits, then the errors.
- Bugfix: first a slice of `keep` cases for the Unchanged criteria: `- keep c3.1a: …`. They must pass on the current code. Then the slices for the Expected criteria: they fail on the current code (red) and pass after the fix.

## Check

Run `python3 <spec.py> check <dir>` (or `check <dir> requirements` after the Requirements section only). Fix each `FAIL` line. Done when it prints `RESULT: PASS`. One exception: while Open questions has items, the line `open questions remain` can stay.
