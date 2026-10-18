import re

from hypothesis import given, settings, strategies as st

from textkit.slug import MAX_LEN, slugify

SHAPE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def test_accents_reduced_to_ascii():
    # Requirement 1.2
    assert slugify("Café") == "cafe"
    assert slugify("Café au lait!") == "cafe-au-lait"


def test_untitled_when_no_ascii_alnum():
    # Requirement 1.5
    assert slugify("") == "untitled"
    assert slugify("!!!") == "untitled"
    assert slugify("日本語") == "untitled"


# Feature: title-slugs, Property 1: Slug shape
@settings(max_examples=100)
@given(st.text())
def test_property_1_slug_shape(title):
    assert SHAPE.match(slugify(title))


# Feature: title-slugs, Property 2: Slug length
@settings(max_examples=100)
@given(st.text(max_size=1000))
def test_property_2_slug_length(title):
    assert len(slugify(title)) <= MAX_LEN


# Feature: title-slugs, Property 3: Slug idempotence
@settings(max_examples=100)
@given(st.text())
def test_property_3_slug_idempotence(title):
    slug = slugify(title)
    assert slugify(slug) == slug
