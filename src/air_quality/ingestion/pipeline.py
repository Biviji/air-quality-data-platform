
from datetime import datetime, timedelta, timezone
from pathlib import Path

from air_quality.ingestion.fetcher import OpenAQFetcher
from air_quality.storage.jsonl_writer import write_jsonl
from air_quality.storage.state import load_watermark, save_watermark
from air_quality.validation.deduplication import deduplicate_measurements


class IngestionPipeline:

    def __init__(
        self,
        fetcher: OpenAQFetcher,
        sensor_id: int,
        project_root: Path,
    ):
        self.fetcher = fetcher
        self.sensor_id = sensor_id
        self.project_root = project_root

        self.state_path = (
            project_root / "data" / "state"
            / f"sensor_{sensor_id}.json"
        )

        self.raw_dir = project_root / "data" / "raw" / "batches"
        self.processed_dir = project_root / "data" / "processed" / "batches"

    def run(self, initial_start: datetime) -> int:

        # 1. Читаем watermark
        watermark = load_watermark(self.state_path)

        if watermark is None:
            start = initial_start
        else:
            start = datetime.fromisoformat(
                watermark.replace("Z", "+00:00")
            )

        if start.tzinfo is None:
            raise ValueError("Start datetime must have timezone")

        start = start.astimezone(timezone.utc)

        # 2. Загружаем максимум один день
        now = datetime.now(timezone.utc)
        end = min(start + timedelta(days=1), now)

        if start >= end:
            print("No new interval to ingest")
            return 0

        # 3. Формируем параметры API
        params = {
            "datetime_from": start.isoformat().replace("+00:00", "Z"),
            "datetime_to": end.isoformat().replace("+00:00", "Z"),
        }

        # 4. Получаем данные
        measurements = self.fetcher.fetch_all(
            endpoint=f"sensors/{self.sensor_id}/measurements",
            params=params,
            page_size=100,
            max_pages=20,
        )

        # 5. Проверяем, не обрезана ли выгрузка
        if len(measurements) == 2000:
            raise RuntimeError(
                "Pagination limit reached; batch may be incomplete"
            )

        # 6. Удаляем дубликаты внутри batch
        unique_measurements = deduplicate_measurements(
            measurements,
            self.sensor_id,
        )

        print(f"Raw records: {len(measurements)}")
        print(f"Unique records: {len(unique_measurements)}")
        print(f"Duplicates removed: {len(measurements) - len(unique_measurements)}")

        # 7. Формируем имя batch-файла
        start_label = start.strftime("%Y%m%dT%H%M%SZ")
        end_label = end.strftime("%Y%m%dT%H%M%SZ")

        output_path = self.raw_dir / (
            f"sensor_{self.sensor_id}_"
            f"{start_label}_{end_label}.jsonl"
        )

        # 8. Сохраняем batch

        temporary_path = output_path.with_suffix(".tmp")

        write_jsonl(measurements, temporary_path)
        temporary_path.replace(output_path)

        processed_path = self.processed_dir / output_path.name
        processed_temp = processed_path.with_suffix(".tmp")

        processed_path.parent.mkdir(parents=True, exist_ok=True)

        write_jsonl(unique_measurements, processed_temp)
        processed_temp.replace(processed_path)

        # 9. Обновляем watermark
        save_watermark(
            self.state_path,
            params["datetime_to"]
        )

        print(f"Raw saved: {output_path}")
        print(f"Processed saved: {processed_path}")
        print(f"Watermark: {params['datetime_to']}")

        return len(unique_measurements)
