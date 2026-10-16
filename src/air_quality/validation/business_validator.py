
from datetime import datetime, timezone
import math


ALLOWED_PARAMETERS = {
    "pm25": "µg/m³",
    "pm10": "µg/m³",
    "pm1": "µg/m³",
    "temperature": "c",
    "relativehumidity": "%",
}


def validate_business_rules(record: dict) -> list[str]:
    errors = []

    parameter = record["parameter"]
    value = record["value"]
    unit = record["unit"]
    measured_at = record["measured_at"]
    coverage = record["coverage_percent"]

    # 1. Проверяем параметр
    if parameter not in ALLOWED_PARAMETERS:
        errors.append(f"Unsupported parameter: {parameter}")
        return errors

    # 2. Проверяем единицу измерения
    expected_unit = ALLOWED_PARAMETERS[parameter]

    if unit != expected_unit:
        errors.append(
            f"Invalid unit for {parameter}: {unit}"
        )

    # 3. Проверяем числовое значение
    if not math.isfinite(value):
        errors.append("value must be finite")
    elif parameter in {"pm25", "pm10", "pm1"} and value < 0:
        errors.append("Particle concentration cannot be negative")
    elif parameter == "relativehumidity" and not 0 <= value <= 100:
        errors.append("Relative humidity must be between 0 and 100")

    # 4. Проверяем coverage
    if coverage is not None:
        if not math.isfinite(coverage) or not 0 <= coverage <= 100:
            errors.append("coverage_percent must be between 0 and 100")

    # 5. Проверяем timestamp
    if measured_at.tzinfo is None:
        errors.append("Timestamp must have timezone")
    elif measured_at > datetime.now(timezone.utc):
        errors.append("Measurement timestamp is in the future")

    return errors
