"""Synthetic pure domain boundary for native static-default verification."""


def label(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TypeError("A non-empty label is required")
    return value.strip()
