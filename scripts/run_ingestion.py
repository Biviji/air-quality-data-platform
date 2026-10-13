
from datetime import datetime, timezone
from pathlib import Path

from air_quality.ingestion.client import OpenAQClient
from air_quality.ingestion.fetcher import OpenAQFetcher
from air_quality.ingestion.pipeline import IngestionPipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]

client = OpenAQClient()
fetcher = OpenAQFetcher(client)

pipeline = IngestionPipeline(
    fetcher=fetcher,
    sensor_id=11760952,
    project_root=PROJECT_ROOT,
)

saved_count = pipeline.run(
    initial_start=datetime(
        2026, 10, 1, 0, 0,
        tzinfo=timezone.utc
    )
)

print("Records saved:", saved_count)
