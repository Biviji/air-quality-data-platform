import json
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "batches"

files = sorted(RAW_DIR.glob("*.jsonl"))

if not files:
    raise FileNotFoundError("No raw batch files found")

file_path = files[-1]

print("Inspecting:", file_path.name)

records = []

with file_path.open("r", encoding="utf-8") as file:
    for line in file:
        if line.strip():
            record = json.loads(line)
            records.append(record)

print("Total records:", len(records))

if not records:
    raise ValueError("Batch is empty")

print("\nFIRST RECORD:")
print(json.dumps(records[0], indent=2, ensure_ascii=False))

print("\nTOP-LEVEL FIELDS:")
for key in records[0]:
    print(key)

print("\nFIELD FREQUENCY:")

field_counts = Counter()

for record in records:
    if isinstance(record, dict):
        field_counts.update(record.keys())

for field, count in field_counts.items():
    print(f"{field}: {count}/{len(records)}")