# Feature: slugify-unique-slug, Property 2: Idempotence
from hypothesis import given, settings, strategies as st

from textkit.slug import slugify


@settings(max_examples=100)
@given(st.text(max_size=10000))
def test_slugify_idempotent(title):
    once = slugify(title)
    assert slugify(once) == once


def test_examples():
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("") == "untitled"
    assert slugify("Café") == "cafe"
    assert slugify(slugify("a" * 49 + " b")) == slugify("a" * 49 + " b")
