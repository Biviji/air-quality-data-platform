from pathlib import Path

from air_quality.transformation.batch_processor import process_batch


PROJECT_ROOT = Path(__file__).resolve().parents[1]

processed_dir = (
    PROJECT_ROOT / "data" / "processed" / "batches"
)

files = sorted(processed_dir.glob("*.jsonl"))

if not files:
    raise FileNotFoundError("No processed batches found")

file_path = files[0]

print(f"Reading file: {file_path.name}")

records = process_batch(
    file_path=file_path,
    sensor_id=11760952,
)

print("\nFirst transformed record:")

if records:
    print(records[0])