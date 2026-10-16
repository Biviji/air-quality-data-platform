from datetime import timezone


UNIT_ALIASES = {
    "ug/m3": "µg/m³",
    "μg/m3": "µg/m³",
    "µg/m3": "µg/m³",
    "µg/m³": "µg/m³",
}


def clean_measurement(record: dict) -> dict:

    cleaned = record.copy()

    # 1. Normalize parameter name
    cleaned["parameter"] = (
        cleaned["parameter"].strip().lower()
    )

    # 2. Normalize unit
    unit = cleaned["unit"].strip()

    cleaned["unit"] = UNIT_ALIASES.get(
        unit,
        unit,
    )

    # 3. Normalize numeric value
    cleaned["value"] = float(cleaned["value"])

    # 4. Normalize timestamp to UTC
    cleaned["measured_at"] = (
        cleaned["measured_at"].astimezone(timezone.utc)
    )

    # 5. Normalize coverage
    if cleaned["coverage_percent"] is not None:
        cleaned["coverage_percent"] = float(
            cleaned["coverage_percent"]
        )

    return cleaned