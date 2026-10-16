
import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from air_quality.transformation.batch_processor import process_batch
from air_quality.quality.quality_report import generate_quality_report


valid = {
    "value": 31.5,
    "parameter": {
        "name": "pm25",
        "units": "µg/m³"
    },
    "period": {
        "datetimeFrom": {
            "utc": "2026-10-08T10:00:00Z"
        }
    },
    "flagInfo": {
        "hasFlags": False
    },
    "coverage": {
        "percentCoverage": 100.0
    }
}

records = []

# 1. Valid measurement
records.append(deepcopy(valid))

# 2. Missing parameter
record = deepcopy(valid)
del record["parameter"]
records.append(record)

# 3. Invalid value type
record = deepcopy(valid)
record["value"] = "hello"
records.append(record)

# 4. Negative PM2.5
record = deepcopy(valid)
record["value"] = -10
records.append(record)

# 5. Invalid coverage
record = deepcopy(valid)
record["coverage"]["percentCoverage"] = 150
records.append(record)

# 6. Invalid timestamp
record = deepcopy(valid)
record["period"]["datetimeFrom"]["utc"] = "not-a-date"
records.append(record)

# 7. Invalid flagInfo structure
record = deepcopy(valid)
record["flagInfo"] = []
records.append(record)


with TemporaryDirectory() as temp_dir:
    file_path = Path(temp_dir) / "invalid_batch.jsonl"

    with file_path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

    accepted, rejected = process_batch(
        file_path=file_path,
        sensor_id=11760952,
    )

    report = generate_quality_report(accepted, rejected)

    print("\nDATA QUALITY REPORT:")
    for key, value in report.items():
        print(f"{key}: {value}")

    print("\nREJECTED RECORDS:")
    for record in rejected:
        print(
            f"Index: {record['index']} | "
            f"Stage: {record['stage']} | "
            f"Errors: {record['errors']}"
        )

    assert len(accepted) == 1
    assert len(rejected) == 6

    print("\nAll checks passed!")
