"""Synthetic boundary cases, not application-foundation assurance."""

import pytest

from example_app.domain import label


def test_label_trims_valid_input() -> None:
    assert label(" example ") == "example"


def test_label_rejects_non_string_input() -> None:
    with pytest.raises(TypeError):
        label(123)
