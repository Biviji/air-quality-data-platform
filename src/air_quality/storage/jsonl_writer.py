
import json
from pathlib import Path


def write_jsonl(records: list[dict], output_path: Path) -> int:

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output_path.open("w", encoding="utf-8") as file:
        for record in records:
            line = json.dumps(record, ensure_ascii=False)
            file.write(line + "\n")

    return len(records)
