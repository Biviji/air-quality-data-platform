from datetime import datetime, timezone

from air_quality.validation.schema_validator import validate_schema


valid_record = {
    "value": 150.4,
    "parameter": "pm25",
    "unit": "µg/m³",
    "measured_at": datetime(2026, 10, 8, tzinfo=timezone.utc),
    "has_flags": False,
    "coverage_percent": 100.0,
}

invalid_record = {
    "value": "hello",
    "parameter": None,
    "unit": 123,
    "measured_at": "yesterday",
    "has_flags": "false",
    "coverage_percent": "unknown",
}

print("VALID RECORD:")
print(validate_schema(valid_record))

print("\nINVALID RECORD:")
print(validate_schema(invalid_record))