# Feature: slugify-unique-slug, Property 1: Slug format
# Validates: Requirements 1.2, 1.3, 1.4, 1.5, 1.6, 1.7
import re

from hypothesis import given, settings
from hypothesis import strategies as st

from textkit.slug import slugify

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


@settings(max_examples=100)
@given(st.text(max_size=10000))
def test_slug_format(title):
    slug = slugify(title)
    assert SLUG_RE.fullmatch(slug)
    assert 1 <= len(slug) <= 50


def test_examples():
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("") == "untitled"
    assert slugify("Café") == "cafe"
    assert slugify("!!!") == "untitled"
    assert slugify("a" * 49 + " b") == "a" * 49
