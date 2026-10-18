# Feature: slugify-unique-slug, Property 5: No mutation
from hypothesis import given, settings, strategies as st

from textkit.slug import unique_slug


@settings(max_examples=100)
@given(st.text(max_size=10000), st.sets(st.text(max_size=100), max_size=100))
def test_unique_slug_does_not_mutate_existing(title, existing):
    before = set(existing)
    unique_slug(title, existing)
    assert existing == before


@settings(max_examples=100)
@given(st.text(max_size=200), st.sets(st.text(max_size=20), max_size=20))
def test_unique_slug_does_not_mutate_when_base_taken(title, existing):
    from textkit.slug import slugify

    existing = existing | {slugify(title), f"{slugify(title)}-2"}
    before = set(existing)
    unique_slug(title, existing)
    assert existing == before


def test_examples():
    existing = {"untitled"}
    assert unique_slug("", existing) == "untitled-2"
    assert existing == {"untitled"}
