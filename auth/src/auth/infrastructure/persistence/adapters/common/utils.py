from typing import Any


def unwrap_filters(**filters: Any) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in filters.items():
        if hasattr(value, "value"):
            result[key] = value.value
        else:
            result[key] = value
    return result
