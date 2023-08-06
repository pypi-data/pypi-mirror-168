"""Utilities to help with type checking JSON data."""

from collections.abc import Mapping, Sequence
from typing import TypeGuard

JSONKey = str
JSONValue = (
    str
    | int
    | float
    | bool
    | None
    # Once mypy is able to handle recursive type aliases, we can replace `object` with
    # `JSONValue` in the next two types
    | Mapping[JSONKey, object]
    | Sequence[object]
)
JSONObject = Mapping[JSONKey, JSONValue]
JSONList = Sequence[JSONValue]
JSON = Mapping[JSONKey, JSONValue]
_JSONSimpleValue = str | int | float | bool | None
_JSONComplexValue = JSONObject | JSONList


def _is_json_key(key: object) -> TypeGuard[JSONKey]:
    """Narrow `object` to `str` type."""
    return isinstance(key, JSONKey)


def _is_json_simple_value(value: object) -> TypeGuard[_JSONSimpleValue]:
    """Narrow `object` to `str | int | float | bool | None` types."""
    return isinstance(value, _JSONSimpleValue)  # type: ignore # possible mypy bug


def _is_json_complex_value(value: object) -> TypeGuard[_JSONComplexValue]:
    """Narrow `object` to `JSONObject | JSONList` types."""
    if isinstance(value, Mapping):
        return is_json(value)
    if isinstance(value, Sequence):
        return all(_is_json_value(maybe_json_value) for maybe_json_value in value)
    return False


def _is_json_value(value: object) -> TypeGuard[JSONValue]:
    """Narrow `object` to `JSONValue` type."""
    return _is_json_simple_value(value) or _is_json_complex_value(value)


def is_json(value: object) -> TypeGuard[JSON]:
    """Narrow `object` to `JSON` type."""
    if not isinstance(value, Mapping):
        return False
    return all(
        _is_json_key(maybe_json_key) and _is_json_value(maybe_json_value)
        for maybe_json_key, maybe_json_value in value.items()
    )


if __name__ == "__main__":
    raise SystemExit(0)
