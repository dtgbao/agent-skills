import re

from hypothesis import given, settings, strategies as st

from textkit.slug import MAX_LEN, slugify

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def test_accents_become_ascii():
    assert slugify("Héllo  World") == "hello-world"
    assert slugify("Crème Brûlée") == "creme-brulee"


def test_compatibility_characters():
    assert slugify("ﬁne ① day") == "fine-1-day"


def test_non_ascii_dropped():
    assert slugify("日本 abc") == "abc"


def test_untitled_when_empty():
    assert slugify("") == "untitled"
    assert slugify("   ") == "untitled"
    assert slugify("!!! ---") == "untitled"
    assert slugify("日本語") == "untitled"


def test_truncate_has_no_trailing_hyphen():
    title = "a" * 49 + " b"
    result = slugify(title)
    assert result == "a" * 49
    assert len(result) <= MAX_LEN


# Feature: slugify, Property 1: Slug shape
@settings(max_examples=100)
@given(st.text())
def test_property_slug_shape(title):
    result = slugify(title)
    assert SLUG_RE.match(result)
    assert len(result) <= MAX_LEN


# Feature: slugify, Property 2: Slugify idempotent
@settings(max_examples=100)
@given(st.text())
def test_property_idempotent(title):
    once = slugify(title)
    assert slugify(once) == once
