
from datetime import datetime, timezone

from air_quality.validation.schema_validator import validate_schema
from air_quality.validation.business_validator import (
    validate_business_rules,
)


records = [
    {
        "value": 150.4,
        "parameter": "pm25",
        "unit": "µg/m³",
        "measured_at": datetime(2026, 10, 8, tzinfo=timezone.utc),
        "has_flags": False,
        "coverage_percent": 100.0,
    },
    {
        "value": -15.0,
        "parameter": "pm25",
        "unit": "µg/m³",
        "measured_at": datetime(2026, 10, 8, tzinfo=timezone.utc),
        "has_flags": False,
        "coverage_percent": 150.0,
    },
    {
        "value": 25.0,
        "parameter": "pm25",
        "unit": "°C",
        "measured_at": datetime(2026, 10, 8, tzinfo=timezone.utc),
        "has_flags": True,
        "coverage_percent": 100.0,
    },
]


for index, record in enumerate(records, start=1):
    errors = validate_schema(record)

    if not errors:
        errors = validate_business_rules(record)

    print(f"Record {index}: {errors}")
