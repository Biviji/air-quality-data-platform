
from air_quality.validation.measurement_validator import validate_batch


measurements = [
    {
        "value": 31.5,
        "period": {
            "datetimeFrom": {
                "utc": "2026-10-01T10:00:00Z"
            }
        },
    },
    {
        "value": "abc",
        "period": {
            "datetimeFrom": {
                "utc": "2026-10-01T11:00:00Z"
            }
        },
    },
    {
        "value": 42.0,
        "period": {
            "datetimeFrom": {
                "utc": "invalid-date"
            }
        },
    },
]

accepted, rejected = validate_batch(measurements)

print("Accepted:", len(accepted))
print("Rejected:", len(rejected))

for item in rejected:
    print(item["errors"])
