
from pathlib import Path

from air_quality.ingestion.client import OpenAQClient
from air_quality.ingestion.fetcher import OpenAQFetcher
from air_quality.storage.jsonl_writer import write_jsonl


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "raw" / "measurements.jsonl"
)

# 1. Создаём API client
client = OpenAQClient()

# 2. Создаём fetcher
fetcher = OpenAQFetcher(client)

# 3. Получаем измерения из OpenAQ
measurements = fetcher.fetch_all(
    endpoint="sensors/11760952/measurements",
    params={
        "datetime_from": "2026-10-01T00:00:00Z",
        "datetime_to": "2026-10-13T00:00:00Z",
    },
    page_size=100,
    max_pages=3
)

print("Total records:", len(measurements))

if measurements:
    print(
        "First timestamp:",
        measurements[0]["period"]["datetimeFrom"]["utc"]
    )

    print(
        "Last timestamp:",
        measurements[-1]["period"]["datetimeFrom"]["utc"]
    )

# 4. Сохраняем данные в JSONL
saved_count = write_jsonl(
    records=measurements,
    output_path=OUTPUT_PATH
)

print(f"\nSaved {saved_count} measurements")
print(f"Output file: {OUTPUT_PATH}")

