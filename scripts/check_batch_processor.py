from pathlib import Path

from air_quality.transformation.batch_processor import process_batch
from air_quality.quality.quality_report import generate_quality_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]

raw_dir = (
    PROJECT_ROOT / "data" / "raw" / "batches"
)

files = sorted(raw_dir.glob("*.jsonl"))

if not files:
    raise FileNotFoundError("No raw batches found")

file_path = files[-1]

print(f"Reading file: {file_path.name}")

accepted, rejected = process_batch(
    file_path=file_path,
    sensor_id=11760952,
)

print("\nPROCESSING RESULTS:")
print("Accepted:", len(accepted))
print("Rejected:", len(rejected))

print("\nFIRST ACCEPTED RECORD:")

if accepted:
    print(accepted[0])

print("\nFIRST REJECTED RECORD:")

if rejected:
    print(rejected[0])

report = generate_quality_report(
    accepted=accepted,
    rejected=rejected,
)

print("\nDATA QUALITY REPORT:")

for key, value in report.items():
    print(f"{key}: {value}")