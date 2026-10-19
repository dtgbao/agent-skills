# sdd

Spec-driven development for Claude Code: a gated spec, then a TDD build that a script drives.

```
(brainstorm) → gate 1: Requirements → gate 2: Design + Plan → spec-run: lanes in parallel → verify
```

Each spec is one file, `docs/specs/<name>/spec.md`. Commit it with the code.

## Install

```text
/plugin marketplace add dtgbao/agent-skills
/plugin install sdd@bao-plugins
```

## Commands

| Command | Does |
|---|---|
| `/sdd:spec-brainstorm [idea]` | Clarify a vague idea: questions, then a playback that you confirm. Writes no files. `spec-new` runs it on vague input |
| `/sdd:spec-new [idea \| name] [--quick]` | Write the spec with the `spec-writer` subagent. Gate 1: requirements and open questions. Gate 2: design and lane plan. `--quick` uses one gate. A name resumes the spec |
| `/sdd:spec-run <name> [lane] [--inline] [--model …] [--effort …]` | One `lane-runner` subagent for each lane, lanes of a wave in parallel. `spec.py` drives each runner one test at a time, then `verify` runs the full suite and checks coverage |
| `/sdd:spec-sync <name>` | After a hand edit: update the affected cases, approve, and reopen the changed cases |

## How the build works

```
spec-run (main) ──► lane-runner A ──► spec.py tdd … run ──► NEXT c1.1a: write ONE test …
                │                      (loop: write → run → read the next step)
                └─► lane-runner B ──► …
            ◄── 3-line report each
spec.py verify: lane state, full suite, criteria coverage, plan ticks
```

`spec.py tdd` is a state machine for each lane. It gives the runner one case at a time and checks the TDD rules itself:

| Rule | How the script enforces it |
|---|---|
| One test at a time | It refuses to run while a test for a later case exists |
| A red is real | An import, name, attribute or call-signature error is a missing name, not a red. The script asks for a stub and runs again |
| Green after red | It records green only after a recorded red, and only when all tests of the lane pass |
| A test that passes at once proves itself | The script tries simple mutants (`<`→`<=`, ±1, `==`→`!=` …) on a temp copy, changed lines first. The case is done only when one mutant fails the test. If none does, the runner gives one with `tdd … mutant` |
| A reopened case changes its test | After a sync, the script refuses the old test text for a changed case |
| Stale tests do not block | The green check skips the tests of open cases; they get their turn |
| Property failures stop the lane | A falsifying example sets the case to `counterexample`. The user chooses: fix code, fix test, or fix the requirement |

The evidence (red line, mutant, time) is in `docs/specs/<name>/.run/<lane>.log`.

## Cost design

| Unit | Context per call (measured) |
|---|---|
| Main session call | about 70k tokens at the start, and it grows |
| Subagent call | about 15k tokens |

Thus the main session only asks you questions, starts subagents and runs `spec.py`. It does not read the spec, the code or the diffs. One runner does a full lane, so it reads the code one time. Lanes own different files, so lanes in one wave cannot clash.

Tiers: lane `Tier` S = haiku, M = sonnet low, L = sonnet medium. A retry goes one tier up, to sonnet high at most. Each TDD cycle is 2 runner calls: (test + run) and (code + run). The writer makes one case for each criterion, and a second case only when it needs new code. `--model` and `--effort` set all lanes.

## State

`.spec.json` holds the phase states (`pending`, `approved`, `stale`), a hash for each section, and the criterion baseline at design approval. `.run/<lane>.json` holds the state of each case.

```bash
python3 shared/scripts/spec.py status docs/specs/<name>   # phases and the next command
python3 shared/scripts/spec.py check docs/specs/<name>    # format, lanes, slices, coverage
python3 shared/scripts/spec.py drift docs/specs/<name>    # hand edits, changed criteria, affected cases
```

A changed case or criterion goes back to `todo` on the next `spec.py` call, so `spec-run` builds it again.

## Layout

```
.claude-plugin/plugin.json, plugin.json
skills/spec-{brainstorm,new,run,sync}/SKILL.md   user-invoked; the main session reads only these
agents/spec-writer.md                            writes and updates spec.md
agents/lane-runner.md                            runs one lane through spec.py tdd
shared/spec-format.md                            the spec.md format (the writer reads it)
shared/glossary.md                               terms
shared/scripts/spec.py                           state, checks, TDD loop, verify (stdlib only)
```

## Design notes

- All instruction files use ASD-STE100 Simplified Technical English. Each term has one meaning, defined in [`shared/glossary.md`](shared/glossary.md).
- All skills set `disable-model-invocation: true`: you type them, and no description sits in context.
- Rules that a model can skip are in `spec.py`, not in prose. This lets a low-effort model follow the process.
- The plan holds literal test cases, not instructions. A small model copies examples well.
- Removed in this version: `spec-analyze` (gate 1 asks about open questions directly), the Design-First and Quick Plan workflows (`--quick` replaces Quick Plan), and the leaf-per-subagent waves.

## Evals

The eval harness, the mock projects and the acceptance suites are in [`evals/sdd/`](../../evals/sdd/README.md).

## Test locally

From the repo root:

```bash
claude --plugin-dir plugins/sdd
```
