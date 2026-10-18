# bugfix.md

Criteria in `${CLAUDE_PLUGIN_ROOT}/shared/ears.md` (Bugfix forms).

Done when:
- repro steps exact: starting state, input, observed result
- every Current item `1.n` has Expected item `2.n` with same condition
- Unchanged items cover every neighbor path user named or investigation exposed
- every item has one observable assertion. Defect with two outcomes → two Current items, each with its Expected item

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

Example, one assertion per item:

```markdown
1.1 WHEN 25 items are paged by 10 THEN the system returns 2 as total_pages
1.2 WHEN page 3 of 25 items paged by 10 is requested THEN the system returns no items
2.1 WHEN 25 items are paged by 10 THE SYSTEM SHALL return 3 as total_pages
2.2 WHEN page 3 of 25 items paged by 10 is requested THE SYSTEM SHALL return items 21–25
```
