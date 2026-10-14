def deduplicate_measurements(measurements, sensor_id):
    seen = set()
    unique = []

    for measurement in measurements:
        period = measurement["period"]
        timestamp = period["datetimeFrom"]["utc"]
        key = (sensor_id, timestamp)
        if key in seen:
            continue

        seen.add(key)
        unique.append(measurement)
    return unique