# Requirements Document

## Introduction

`textkit` gains a slug module. `slugify(title)` turns a blog post title into a URL slug. `unique_slug(title, existing)` returns a slug that is not yet taken. Blog engine code calls both functions.

Assumptions (from Quick Plan questions):
- Slugs are ASCII only. Input is NFKD-normalized and non-ASCII characters are dropped.
- An empty title, or a title with no ASCII letter or digit, gives the slug `untitled`.
- `existing` is a `set[str]`. The Title is a `str` of 0–10000 characters. `existing` holds 0–10000 entries.
- The 40-character limit applies to `slugify` output only. `unique_slug` appends the suffix after that limit, so its result can be longer than 40 characters.
- Stack: Python stdlib, Hypothesis for property tests.

## Glossary

- **textkit**: the Python package in `textkit/`.
- **slugify**: the function `textkit.slug.slugify(title: str) -> str`.
- **unique_slug**: the function `textkit.slug.unique_slug(title: str, existing: set[str]) -> str`.
- **Title**: the `str` input of `slugify` and `unique_slug`.
- **Slug**: a `str` of lowercase ASCII letters, digits and single hyphens. It does not start or end with a hyphen.
- **Existing**: the `set[str]` of Slugs already in use.

## Requirements

### Requirement 1: Slugify a title

**User Story:** As a blog author, I want a title converted to a clean URL slug, so that post URLs are readable and stable.

#### Acceptance Criteria

1. WHEN slugify receives a Title, THE slugify SHALL NFKD-normalize the Title and drop every non-ASCII character before any other step.
2. WHEN slugify receives a Title, THE slugify SHALL return a Slug that contains only lowercase letters `a-z`, digits `0-9` and hyphens.
3. WHEN a Title contains a run of one or more non-alphanumeric characters, THE slugify SHALL replace each run with exactly one hyphen.
4. THE slugify SHALL return a Slug that does not start with a hyphen and does not end with a hyphen.
5. THE slugify SHALL return a Slug of 1–40 characters.
6. IF a Title is empty or has no ASCII letter or digit after normalization, THEN THE slugify SHALL return `untitled`.
7. WHEN truncation to 40 characters leaves a trailing hyphen, THE slugify SHALL remove that hyphen.

### Requirement 2: Make a slug unique

**User Story:** As a blog author, I want a slug that does not collide with an existing post, so that every post has its own URL.

#### Acceptance Criteria

1. WHEN slugify(Title) is not in Existing, THE unique_slug SHALL return slugify(Title).
2. WHEN slugify(Title) is in Existing, THE unique_slug SHALL return slugify(Title) followed by `-N`, where N is the smallest integer ≥ 2 that gives a value not in Existing.
3. THE unique_slug SHALL return a value that is not in Existing.
4. THE unique_slug SHALL leave Existing unchanged.
5. IF Existing is empty, THEN THE unique_slug SHALL return slugify(Title).
6. IF a Title is empty and `untitled` is in Existing, THEN THE unique_slug SHALL return `untitled-2` when `untitled-2` is not in Existing.
