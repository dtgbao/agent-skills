---
title: Use Property-Based Testing for Broad Invariants
impact: MEDIUM
tags: testing, hypothesis, properties, validation
---

## Use Property-Based Testing for Broad Invariants

When Hypothesis is already installed or explicitly requested, express stable invariants over a broad
input domain and let it generate, replay, and shrink counterexamples. Keep strategies valid by
construction; use example-based tests for named business scenarios and property tests for algebraic,
serialization, normalization, and validation invariants.

**Incorrect:**

```python
def test_item_round_trip() -> None:
    for quantity in [1, 2, 100]:
        item = Item(name="keyboard", quantity=quantity)
        assert Item.model_validate_json(item.model_dump_json()) == item
```

**Correct:**

```python
from hypothesis import example, given, strategies as st
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    quantity: int = Field(ge=1, le=10_000)


valid_names = st.text(
    alphabet=st.characters(blacklist_categories=("Cs",)),
    min_size=1,
    max_size=100,
)


def normalize_email(value: str) -> str:
    return value.casefold()


@example(name="keyboard", quantity=1)
@given(
    name=valid_names,
    quantity=st.integers(min_value=1, max_value=10_000),
)
def test_item_json_round_trip_preserves_model(
    name: str,
    quantity: int,
) -> None:
    item = Item(name=name, quantity=quantity)

    restored = Item.model_validate_json(item.model_dump_json())

    assert restored == item


@given(value=st.text())
def test_normalize_email_is_idempotent(value: str) -> None:
    once = normalize_email(value)
    assert normalize_email(once) == once
```

Choose the full valid domain rather than tuning probability distributions. Avoid shared mutable
function-scoped fixtures: Hypothesis runs the test many times while pytest normally creates the
fixture once for that test invocation. Use generated values to build fresh state per example.

**Compatibility:** Apply only when Hypothesis is detected or requested. The example targets Pydantic
2 serialization APIs. Bound expensive integration properties and keep deterministic regression
examples for previously found bugs.

References:

- [Hypothesis: Quickstart](https://hypothesis.readthedocs.io/en/latest/quickstart.html)
- [Hypothesis: Strategies](https://hypothesis.readthedocs.io/en/latest/reference/strategies.html)
- [Hypothesis: pytest compatibility](https://hypothesis.readthedocs.io/en/latest/compatibility.html#pytest)
- [Pydantic: Serialization](https://docs.pydantic.dev/latest/concepts/serialization/)
