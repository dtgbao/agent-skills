# Requirements Document

## Introduction

Add `slugify(title)` and `unique_slug(title, existing)` to `textkit`. Blog authors use them to make URL slugs from titles. A Slug has at most 40 characters.

Assumptions (from user answers):
- Non-ASCII letters are reduced to ASCII with Unicode NFKD decomposition. Characters that stay non-ASCII are dropped.
- An empty Slug becomes `untitled`.
- `existing` is a `set[str]` of slugs already in use.
- Property tests use Hypothesis.

## Glossary

- **Title**: input `str` of 0–1000 characters.
- **Slug**: `str` of lowercase ASCII letters, digits and single hyphens, 1–40 characters.
- **Slug_Generator**: function `slugify(title)` in `textkit/slug.py`.
- **Unique_Slug_Generator**: function `unique_slug(title, existing)` in `textkit/unique.py`.
- **Existing_Set**: `set[str]` of Slugs already in use.

## Requirements

### Requirement 1: Make a slug from a title

**User Story:** As a blog author, I want a URL-safe slug from a title, so that I can build post URLs.

#### Acceptance Criteria

1. THE Slug_Generator SHALL return a Slug that contains only the characters `a-z`, `0-9` and `-`.
2. WHEN a Title contains accented letters, THE Slug_Generator SHALL reduce them to their ASCII base letters with NFKD decomposition ("Café" gives "cafe").
3. THE Slug_Generator SHALL return a Slug with no leading hyphen, no trailing hyphen and no two hyphens in a row.
4. THE Slug_Generator SHALL return a Slug of at most 40 characters.
5. IF a Title has no ASCII letter or digit after normalization, THEN THE Slug_Generator SHALL return "untitled".
6. WHEN the Slug_Generator receives its own output as a Title, THE Slug_Generator SHALL return the same Slug.

### Requirement 2: Make a slug that is not in use

**User Story:** As a blog author, I want a slug that no other post uses, so that post URLs do not clash.

#### Acceptance Criteria

1. WHEN the Slug of a Title is not in the Existing_Set, THE Unique_Slug_Generator SHALL return that Slug.
2. IF the Slug of a Title is in the Existing_Set, THEN THE Unique_Slug_Generator SHALL return the Slug with the smallest suffix `-N` (N ≥ 2) that is not in the Existing_Set.
3. THE Unique_Slug_Generator SHALL return a Slug of at most 40 characters, suffix included.
4. THE Unique_Slug_Generator SHALL leave the Existing_Set unchanged.
5. IF the Title has no ASCII letter or digit and "untitled" is in the Existing_Set, THEN THE Unique_Slug_Generator SHALL return "untitled-2" or the next free suffix.

## Open Questions

- none
