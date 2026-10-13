
import json
from pathlib import Path


def load_watermark(state_path: Path) -> str | None:
    if not state_path.exists():
        return None

    with state_path.open("r", encoding="utf-8") as file:
        state = json.load(file)

    return state.get("last_successful_timestamp")


def save_watermark(state_path: Path, timestamp: str) -> None:
    state_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    state = {
        "last_successful_timestamp": timestamp
    }

    with state_path.open("w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)
