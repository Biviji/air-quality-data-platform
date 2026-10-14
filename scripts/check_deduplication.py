from air_quality.validation.deduplication import (
    deduplicate_measurements,
)

measurements = [
    {"period":
         {"datetimeFrom":
              {"utc": "2026-10-01T10:00:00Z"}
          },
     "value": 31},
    {"period":
         {"datetimeFrom":
              {"utc": "2026-10-01T11:00:00Z"}
          },
     "value": 35},
    {"period":
         {"datetimeFrom":
              {"utc": "2026-10-01T10:00:00Z"}
          },
     "value": 31},
]

result = deduplicate_measurements(
    measurements,
    sensor_id=11760952,
)

print("Before:", len(measurements))
print("After:", len(result))