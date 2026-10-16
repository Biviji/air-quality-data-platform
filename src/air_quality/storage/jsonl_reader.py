import json
from pathlib import Path


def read_jsonl(file_path: Path) -> list[dict]:

    records = []

    with file_path.open("r", encoding="utf-8") as file:

        for line in file:

            if not line.strip():
                continue

            record = json.loads(line)

            records.append(record)

    return records