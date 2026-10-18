# Feature: slugify-unique-slug, Property 4: Smallest free slug
from hypothesis import given, settings, strategies as st

from textkit.slug import slugify, unique_slug


@st.composite
def title_and_existing(draw):
    title = draw(st.text(max_size=10000))
    base = slugify(title)
    # Random strings plus structured candidates so collisions are common.
    noise = draw(st.sets(st.text(max_size=60), max_size=50))
    candidates = [base] + [f"{base}-{n}" for n in range(2, 12)]
    picked = draw(st.sets(st.sampled_from(candidates)))
    return title, noise | picked


@settings(max_examples=200)
@given(title_and_existing())
def test_unique_slug_smallest_free(args):
    title, existing = args
    base = slugify(title)
    result = unique_slug(title, existing)

    assert result not in existing
    if result == base:
        return
    prefix = base + "-"
    assert result.startswith(prefix)
    suffix = result[len(prefix):]
    assert suffix.isdigit() and str(int(suffix)) == suffix
    n = int(suffix)
    assert n >= 2
    assert base in existing
    for k in range(2, n):
        assert f"{base}-{k}" in existing


@settings(max_examples=100)
@given(st.text(max_size=10000))
def test_empty_existing_returns_base(title):
    assert unique_slug(title, set()) == slugify(title)


def test_examples():
    assert unique_slug("Hello", set()) == "hello"
    assert unique_slug("Hello", {"hello"}) == "hello-2"
    assert unique_slug("Hello", {"hello", "hello-2", "hello-3"}) == "hello-4"
    assert unique_slug("Hello", {"hello", "hello-3"}) == "hello-2"
    assert unique_slug("", {"untitled"}) == "untitled-2"
    assert unique_slug("", {"untitled", "untitled-2"}) == "untitled-3"
