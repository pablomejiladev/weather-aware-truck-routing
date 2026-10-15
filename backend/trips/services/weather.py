from datetime import datetime, timezone

import requests

FORECAST = "https://api.open-meteo.com/v1/forecast"
BATCH = 100


def _chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def fetch_hourly(points, forecast_days=3):
    out = []
    for chunk in _chunks(points, BATCH):
        lats = ",".join(f"{p['lat']:.4f}" for p in chunk)
        lons = ",".join(f"{p['lon']:.4f}" for p in chunk)
        resp = requests.get(
            FORECAST,
            params={
                "latitude": lats,
                "longitude": lons,
                "hourly": "wind_speed_10m,rain,snowfall",
                "wind_speed_unit": "mph",
                "precipitation_unit": "inch",
                "timezone": "UTC",
                "forecast_days": forecast_days,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict):
            data = [data]
        for d in data:
            h = d["hourly"]
            out.append({
                "time": h["time"],
                "wind": h["wind_speed_10m"],
                "rain": h["rain"],
                "snow": h["snowfall"],
            })
    return out


def _parse(t):
    return datetime.fromisoformat(t).replace(tzinfo=timezone.utc)


def index_for_time(times, target):
    best_i, best = 0, None
    for i, t in enumerate(times):
        delta = abs((_parse(t) - target).total_seconds())
        if best is None or delta < best:
            best, best_i = delta, i
    return best_i
