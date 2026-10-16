from datetime import datetime


def transform_measurement(
    measurement: dict,
    sensor_id: int,
) -> dict:

    parameter = measurement["parameter"]
    period = measurement["period"]

    timestamp = period["datetimeFrom"]["utc"]

    measured_at = datetime.fromisoformat(
        timestamp.replace("Z", "+00:00")
    )

    transformed = {
        "sensor_id": sensor_id,
        "value": measurement["value"],
        "parameter": parameter["name"],
        "unit": parameter["units"],
        "measured_at": measured_at,
    }

    return transformed

def transform_batch(
    measurements: list[dict],
    sensor_id: int,
) -> list[dict]:

    transformed = []

    for measurement in measurements:
        result = transform_measurement(
            measurement,
            sensor_id,
        )

        transformed.append(result)

    return transformed