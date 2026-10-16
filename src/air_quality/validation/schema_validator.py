from datetime import datetime


def validate_schema(record: dict) -> list[str]:

    errors = []

    required_fields = [
        "value",
        "parameter",
        "unit",
        "measured_at",
        "has_flags",
        "coverage_percent",
    ]

    for field in required_fields:
        if field not in record:
            errors.append(f"Missing required field: {field}")

    if errors:
        return errors

    if (
        isinstance(record["value"], bool)
        or not isinstance(record["value"], (int, float))
    ):
        errors.append("value must be numeric")

    if not isinstance(record["parameter"], str):
        errors.append("parameter must be a string")

    if not isinstance(record["unit"], str):
        errors.append("unit must be a string")

    if not isinstance(record["measured_at"], datetime):
        errors.append("measured_at must be datetime")

    if not isinstance(record["has_flags"], bool):
        errors.append("has_flags must be boolean")

    if (
        record["coverage_percent"] is not None
        and (
            isinstance(record["coverage_percent"], bool)
            or not isinstance(record["coverage_percent"], (int, float))
        )
    ):
        errors.append("coverage_percent must be numeric or None")

    return errors