from datetime import datetime, timezone, timedelta

from air_quality.validation.schema_validator import validate_schema
from air_quality.transformation.measurement_cleaner import (
    clean_measurement,
)
from air_quality.validation.business_validator import (
    validate_business_rules,
)


record = {
    "value": 31,
    "parameter": " PM25 ",
    "unit": "ug/m3",
    "measured_at": datetime(
        2026, 10, 8, 8, 0,
        tzinfo=timezone(timedelta(hours=8))
    ),
    "has_flags": False,
    "coverage_percent": 100,
}

print("BEFORE:")
print(record)

schema_errors = validate_schema(record)

if schema_errors:
    print("SCHEMA ERRORS:", schema_errors)
else:
    cleaned = clean_measurement(record)

    print("\nAFTER:")
    print(cleaned)

    print("\nBUSINESS ERRORS:")
    print(validate_business_rules(cleaned))