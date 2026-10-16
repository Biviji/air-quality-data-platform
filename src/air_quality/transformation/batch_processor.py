from pathlib import Path

from air_quality.storage.jsonl_reader import read_jsonl
from air_quality.parsing.measurement_parser import parse_measurement
from air_quality.validation.schema_validator import validate_schema
from air_quality.validation.business_validator import validate_business_rules
from air_quality.transformation.measurement_cleaner import clean_measurement


def process_batch(
    file_path: Path,
    sensor_id: int,
) -> tuple[list[dict], list[dict]]:

    measurements = read_jsonl(file_path)

    print(f"Loaded records: {len(measurements)}")

    accepted = []
    rejected = []

    for index, measurement in enumerate(measurements):

        # 1. Parsing
        try:
            parsed = parse_measurement(measurement)

        except (ValueError, TypeError, AttributeError) as exc:
            rejected.append({
                "index": index,
                "stage": "parsing",
                "original": measurement,
                "errors": [str(exc)],
            })
            continue

        # 2. Schema Validation
        schema_errors = validate_schema(parsed)

        if schema_errors:
            rejected.append({
                "index": index,
                "stage": "schema",
                "original": measurement,
                "errors": schema_errors,
            })
            continue

        # 3. Cleaning
        try:
            cleaned = clean_measurement(parsed)

        except (ValueError, TypeError, AttributeError) as exc:
            rejected.append({
                "index": index,
                "stage": "cleaning",
                "original": measurement,
                "errors": [str(exc)],
            })
            continue

        # 4. Business Validation
        business_errors = validate_business_rules(cleaned)

        if business_errors:
            rejected.append({
                "index": index,
                "stage": "business",
                "original": measurement,
                "errors": business_errors,
            })
            continue

        # 5. Accepted
        cleaned["sensor_id"] = sensor_id
        accepted.append(cleaned)

    print(f"Accepted records: {len(accepted)}")
    print(f"Rejected records: {len(rejected)}")

    return accepted, rejected