from hypothesis import given, settings, strategies as st

from textkit.slug import MAX_LEN, slugify
from textkit.unique import unique_slug


def test_untitled_taken_gets_suffix():
    # Requirement 2.5
    assert unique_slug("!!!", {"untitled"}) == "untitled-2"
    assert unique_slug("", {"untitled", "untitled-2"}) == "untitled-3"


@st.composite
def title_and_existing(draw):
    # Long titles reach the 40-character limit so suffix truncation runs.
    title = draw(st.one_of(st.text(), st.text(alphabet="ab -", min_size=45, max_size=70)))
    slug = slugify(title)
    extra = draw(st.sets(st.text()))
    # Include the title's slug and some of its suffixed forms to force collisions.
    include_slug = draw(st.booleans())
    suffixes = draw(st.sets(st.integers(min_value=2, max_value=12)))
    existing = set(extra)
    if include_slug:
        existing.add(slug)
        for n in suffixes:
            suffix = f"-{n}"
            existing.add(slug[: MAX_LEN - len(suffix)].rstrip("-") + suffix)
    return title, existing


# Feature: title-slugs, Property 4: Uniqueness
@settings(max_examples=100)
@given(title_and_existing())
def test_property_4_uniqueness(args):
    title, existing = args
    before = set(existing)
    slug = slugify(title)
    result = unique_slug(title, existing)
    assert result not in existing
    if slug not in existing:
        assert result == slug
    else:
        # Smallest suffix: every smaller suffix is taken.
        n = int(result.rsplit("-", 1)[1])
        assert n >= 2
        for k in range(2, n):
            suffix = f"-{k}"
            assert slug[: MAX_LEN - len(suffix)].rstrip("-") + suffix in existing
    assert existing == before


# Feature: title-slugs, Property 5: Unique slug length
@settings(max_examples=100)
@given(title_and_existing())
def test_property_5_unique_slug_length(args):
    title, existing = args
    assert len(unique_slug(title, existing)) <= MAX_LEN
