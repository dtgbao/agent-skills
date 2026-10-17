# bugfix.md

Criteria in `${CLAUDE_PLUGIN_ROOT}/shared/ears.md` (Bugfix forms).

Done when:
- repro steps exact: starting state, input, observed result
- every Current item `1.n` has Expected item `2.n` with same condition
- Unchanged items cover every neighbor path user named or code read exposed
- every item has one observable assertion

Skeleton:

```markdown
# Bugfix Requirements Document

## Introduction

<bug summary, impact, repro steps>

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN <condition> THEN the system <incorrect behavior>

### Expected Behavior (Correct)

2.1 WHEN <condition> THE SYSTEM SHALL <correct behavior>

### Unchanged Behavior (Regression Prevention)

3.1 WHEN <condition> THE SYSTEM SHALL CONTINUE TO <existing behavior>
```
