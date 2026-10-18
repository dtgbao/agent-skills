from hypothesis import given, settings, strategies as st

from textkit.slug import MAX_LEN, slugify
from textkit.unique import unique_slug

SLUG_TEXT = st.text(alphabet="ab-", min_size=1, max_size=MAX_LEN)


def test_free_slug_returned():
    assert unique_slug("Hello World", set()) == "hello-world"
    assert unique_slug("Hello World", {"other"}) == "hello-world"


def test_taken_slug_gets_suffix_2():
    assert unique_slug("Hello World", {"hello-world"}) == "hello-world-2"


def test_taken_slug_skips_used_suffixes():
    existing = {"hello-world", "hello-world-2", "hello-world-3"}
    assert unique_slug("Hello World", existing) == "hello-world-4"


def test_taken_long_slug_stays_within_limit():
    base = slugify("a" * 80)
    assert len(base) == MAX_LEN
    result = unique_slug("a" * 80, {base})
    assert len(result) <= MAX_LEN
    assert result.endswith("-2")


@st.composite
def title_and_existing(draw):
    title = draw(st.text())
    base = slugify(title)
    pool = [base] + [f"{base[: MAX_LEN - len(f'-{n}')].rstrip('-')}-{n}" for n in range(2, 12)]
    taken = draw(st.sets(st.sampled_from(pool)))
    extra = draw(st.sets(st.one_of(st.text(), SLUG_TEXT)))
    return title, taken | extra


# Feature: slugify, Property 3: Unique result
@settings(max_examples=100)
@given(title_and_existing())
def test_property_unique_result(args):
    title, existing = args
    before = set(existing)
    result = unique_slug(title, existing)
    assert result not in existing
    assert len(result) <= MAX_LEN
    assert existing == before


# Feature: slugify, Property 4: Empty set equals slugify
@settings(max_examples=100)
@given(st.text())
def test_property_empty_set_equals_slugify(title):
    assert unique_slug(title, set()) == slugify(title)
