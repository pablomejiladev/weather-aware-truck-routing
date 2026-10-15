import math

EARTH_MILES = 3958.8


def haversine_miles(a, b):
    lon1, lat1 = a
    lon2, lat2 = b
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_MILES * math.asin(math.sqrt(h))


def sample_checkpoints(geometry, interval_miles):
    points = [(c[0], c[1]) for c in geometry]
    checkpoints = [{"lon": points[0][0], "lat": points[0][1], "mile": 0.0}]

    acc = 0.0
    next_mark = interval_miles
    for i in range(1, len(points)):
        a, b = points[i - 1], points[i]
        seg = haversine_miles(a, b)
        while seg > 0 and acc + seg >= next_mark:
            t = (next_mark - acc) / seg
            lon = a[0] + (b[0] - a[0]) * t
            lat = a[1] + (b[1] - a[1]) * t
            checkpoints.append({"lon": lon, "lat": lat, "mile": next_mark})
            next_mark += interval_miles
        acc += seg

    total = acc
    if total - checkpoints[-1]["mile"] > 0.5:
        checkpoints.append({"lon": points[-1][0], "lat": points[-1][1], "mile": total})

    return checkpoints, total
