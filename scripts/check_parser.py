import json
from pathlib import Path

from air_quality.parsing.measurement_parser import (
    parse_measurement,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "batches"

files = sorted(RAW_DIR.glob("*.jsonl"))

if not files:
    raise FileNotFoundError("No raw files found")

file_path = files[-1]

parsed_records = []
failed_records = []

with file_path.open("r", encoding="utf-8") as file:

    for line_number, line in enumerate(file, start=1):

        if not line.strip():
            continue

        try:
            measurement = json.loads(line)

            parsed = parse_measurement(measurement)

            parsed_records.append(parsed)

        except (ValueError, TypeError, AttributeError) as exc:
            failed_records.append({
                "line": line_number,
                "error": str(exc),
            })


print("Total parsed:", len(parsed_records))
print("Total failed:", len(failed_records))

if parsed_records:
    print("\nFIRST PARSED RECORD:")
    print(parsed_records[0])

if failed_records:
    print("\nFAILED RECORDS:")
    for failure in failed_records:
        print(failure)