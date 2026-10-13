from pathlib import Path

from air_quality.storage.state import load_watermark, save_watermark


state_path = Path("data/state/watermark.json")

print("Before:", load_watermark(state_path))

save_watermark(
    state_path,
    "2026-10-12T23:00:00Z"
)

print("After:", load_watermark(state_path))