from pathlib import Path

from air_quality.storage.jsonl_reader import read_jsonl
from air_quality.transformation.measurement_transformer import (
    transform_batch,
)


def process_batch(
    file_path: Path,
    sensor_id: int,
) -> list[dict]:

    # 1. Читаем файл
    measurements = read_jsonl(file_path)

    print(f"Loaded records: {len(measurements)}")

    # 2. Преобразуем записи
    transformed = transform_batch(
        measurements,
        sensor_id,
    )

    print(f"Transformed records: {len(transformed)}")

    # 3. Возвращаем результат
    return transformed