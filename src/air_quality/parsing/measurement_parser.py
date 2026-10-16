from datetime import datetime

def parse_measurement(measurement: dict) -> dict:

    parameter = measurement.get("parameter")
    period = measurement.get("period")

    if not isinstance(parameter, dict):
        raise ValueError("parameter must be an object")

    if not isinstance(period, dict):
        raise ValueError("period must be an object")

    datetime_from = period.get("datetimeFrom")

    if not isinstance(datetime_from, dict):
        raise ValueError("datetimeFrom must be an object")

    timestamp = datetime_from.get("utc")

    if not isinstance(timestamp, str):
        raise ValueError("UTC timestamp must be a string")

    try:
        measured_at = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise ValueError(
            f"Invalid timestamp: {timestamp}"
        ) from exc

    if measured_at.tzinfo is None:
        raise ValueError("Timestamp must contain timezone")

    flag_info = measurement.get("flagInfo")
    coverage = measurement.get("coverage")

    if flag_info is not None and not isinstance(flag_info, dict):
        raise ValueError("flagInfo must be an object or null")

    if coverage is not None and not isinstance(coverage, dict):
        raise ValueError("coverage must be an object or null")

    parsed = {
        "value": measurement.get("value"),
        "parameter": parameter.get("name"),
        "unit": parameter.get("units"),
        "measured_at": measured_at,
                "has_flags": (
            flag_info.get("hasFlags")
            if flag_info is not None
            else None
        ),
        "coverage_percent": (
            coverage.get("percentCoverage")
            if coverage is not None
            else None
        ),
    }

    return parsed