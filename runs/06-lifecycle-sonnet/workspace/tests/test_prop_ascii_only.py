# Feature: slugify-unique-slug, Property 3: Non-ASCII is dropped
# Validates: Requirements 1.1
from hypothesis import given, settings, strategies as st

from textkit.slug import slugify

cjk = st.text(
    alphabet=st.characters(min_codepoint=0x4E00, max_codepoint=0x9FFF),
    max_size=100,
)


@settings(max_examples=100)
@given(title=st.text(max_size=200), c=cjk)
def test_cjk_suffix_is_dropped(title, c):
    assert slugify(title + c) == slugify(title)


def test_examples():
    assert slugify("Café") == "cafe"
    assert slugify("Hello 世界") == "hello"
    assert slugify("世界") == "untitled"
