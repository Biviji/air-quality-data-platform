from air_quality.transformation.measurement_transformer import (
    transform_measurement,
    transform_batch,
)


measurement = {
    "value": 31.0,
    "parameter": {
        "name": "pm25",
        "units": "µg/m³",
    },
    "period": {
        "datetimeFrom": {
            "utc": "2026-10-08T10:00:00Z"
        }
    },
}

result = transform_measurement(
    measurement=measurement,
    sensor_id=11760952,
)

print(result)
print(type(result["measured_at"]))

measurements = [measurement, measurement, measurement]

results = transform_batch(
    measurements,
    sensor_id=11760952,
)

print("Total transformed:", len(results))

for result in results:
    print(result)