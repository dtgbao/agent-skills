# Requirements Document

## Introduction

`textkit` gets two helpers for the blog engine: `slugify(title)` turns a title into a URL slug. `unique_slug(title, existing)` makes a slug that is not yet used. Assumptions: output is ASCII only (accents removed via NFKD); an empty result becomes `untitled`; `existing` is a `set[str]`.

## Glossary

- **Slugifier**: the `slugify` function in `textkit.slug`.
- **Slug_Allocator**: the `unique_slug` function in `textkit.unique`.
- **Slug**: a string of lowercase ASCII letters and digits, joined by single hyphens.
- **Title**: input text, any Unicode string.
- **Existing_Set**: a `set[str]` of slugs already in use.

## Requirements

### Requirement 1: Slugify a title

**User Story:** As a blog author, I want a URL slug made from my title, so that the post has a clean link.

#### Acceptance Criteria

1. WHEN a Title is given, THE Slugifier SHALL return a Slug made of lowercase ASCII letters, digits and single hyphens only.
2. WHEN a Title has accented or compatibility characters, THE Slugifier SHALL convert them to ASCII with NFKD normalization and drop characters that stay non-ASCII.
3. THE Slugifier SHALL return a Slug of at most 40 characters with no leading or trailing hyphen.
4. IF a Title yields no letters or digits, THEN THE Slugifier SHALL return `untitled`.
5. WHEN `slugify` is applied to its own output, THE Slugifier SHALL return the same Slug.

### Requirement 2: Unique slug

**User Story:** As a blog author, I want a slug that no other post uses, so that links never clash.

#### Acceptance Criteria

1. WHEN the Slug of a Title is not in the Existing_Set, THE Slug_Allocator SHALL return that Slug.
2. WHEN the Slug of a Title is in the Existing_Set, THE Slug_Allocator SHALL return a Slug with suffix `-N` (N an integer from 2 up) that is not in the Existing_Set.
3. THE Slug_Allocator SHALL return a Slug of at most 40 characters, including the suffix.
4. THE Slug_Allocator SHALL leave the Existing_Set unchanged.
5. IF the Existing_Set is empty, THEN THE Slug_Allocator SHALL return the same Slug as the Slugifier.

## Open Questions

- none
