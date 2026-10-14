
from datetime import datetime


def validate_measurement(measurement):
    errors = []

    # 1. Проверяем значение
    value = measurement.get("value")

    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
    ):
        errors.append("value must be numeric")

    # 2. Проверяем timestamp
    period = measurement.get("period")

    if not isinstance(period, dict):
        errors.append("period must be an object")
    else:
        datetime_from = period.get("datetimeFrom")

        if not isinstance(datetime_from, dict):
            errors.append("datetimeFrom is missing")
        else:
            timestamp = datetime_from.get("utc")

            if not isinstance(timestamp, str):
                errors.append("timestamp must be a string")
            else:
                try:
                    parsed = datetime.fromisoformat(
                        timestamp.replace("Z", "+00:00")
                    )

                    if parsed.tzinfo is None:
                        errors.append("timestamp must have timezone")

                except ValueError:
                    errors.append("invalid timestamp")

    return errors


def validate_batch(measurements):
    accepted = []
    rejected = []

    for measurement in measurements:
        errors = validate_measurement(measurement)

        if errors:
            rejected.append({
                "record": measurement,
                "errors": errors,
            })
        else:
            accepted.append(measurement)

    return accepted, rejected
