from datetime import datetime, timedelta, timezone

from . import geocode as geocode_mod
from . import routing as routing_mod
from . import weather as weather_mod
from .geometry import sample_checkpoints
from .risk import checkpoint_risk

CORRIDOR_HOURS = 48


def plan_trip(origin_q, dest_q, departure, load_lb, interval_miles):
    origin = geocode_mod.geocode(origin_q)
    dest = geocode_mod.geocode(dest_q)

    routes = routing_mod.get_routes(origin, dest, max_routes=3)
    if not routes:
        raise ValueError("No drivable route was found between those locations.")

    sampled = []
    all_points = []
    for r in routes:
        cps, total_mi = sample_checkpoints(r["geometry"], interval_miles)
        r["total_miles"] = total_mi
        sampled.append(cps)
        all_points.extend(cps)

    now = datetime.now(timezone.utc)
    days_ahead = max(0, (departure - now).days)
    forecast_days = min(16, days_ahead + 3)
    forecast = weather_mod.fetch_hourly(all_points, forecast_days=forecast_days)

    route_wx = []
    cursor = 0
    for cps in sampled:
        route_wx.append(forecast[cursor:cursor + len(cps)])
        cursor += len(cps)

    out_routes = [
        _build_route(r, cps, wx, departure, load_lb)
        for r, cps, wx in zip(routes, sampled, route_wx)
    ]

    best = _pick_best(out_routes)
    for r in out_routes:
        r["recommended"] = r["index"] == best

    corridor = _build_corridor(sampled[best], route_wx[best], departure, load_lb)

    return {
        "origin": origin,
        "destination": dest,
        "departure": departure.isoformat(),
        "load_lb": load_lb,
        "interval_miles": interval_miles,
        "recommended_index": best,
        "routes": out_routes,
        "corridor": corridor,
    }


def _build_route(r, cps, wx, departure, load_lb):
    total_mi = r["total_miles"]
    duration_s = r["duration_s"]

    checkpoints = []
    for i, cp in enumerate(cps):
        frac = cp["mile"] / total_mi if total_mi else 0.0
        eta = departure + timedelta(seconds=duration_s * frac)
        w = wx[i]
        idx = weather_mod.index_for_time(w["time"], eta)
        wind = w["wind"][idx] or 0.0
        rain = w["rain"][idx] or 0.0
        snow = w["snow"][idx] or 0.0
        risk = checkpoint_risk(wind, rain, snow, load_lb)
        checkpoints.append({
            "lat": round(cp["lat"], 5),
            "lon": round(cp["lon"], 5),
            "mile": round(cp["mile"], 1),
            "eta": eta.isoformat(),
            "wind": round(wind, 1),
            "rain": round(rain, 3),
            "snow": round(snow, 3),
            "wind_level": risk["wind_level"],
            "rain_level": risk["rain_level"],
            "snow_level": risk["snow_level"],
            "risk": risk["overall"],
            "score": risk["score"],
        })

    return {
        "index": r["index"],
        "distance_miles": round(total_mi, 1),
        "duration_hours": round(duration_s / 3600, 2),
        "geometry": [[round(c[0], 5), round(c[1], 5)] for c in r["geometry"]],
        "checkpoints": checkpoints,
        "summary": _summarize(checkpoints, total_mi, duration_s),
    }


def _summarize(checkpoints, total_mi, duration_s):
    severe = high = notravel = 0.0
    score_sum = 0.0
    for i, cp in enumerate(checkpoints):
        seg = checkpoints[i + 1]["mile"] - cp["mile"] if i + 1 < len(checkpoints) else 0.0
        if cp["risk"] == "Severe":
            severe += seg
        elif cp["risk"] == "High":
            high += seg
        elif cp["risk"] == "No Travel":
            notravel += seg
        score_sum += cp["score"]

    avg = score_sum / len(checkpoints) if checkpoints else 0.0
    return {
        "no_travel_miles": round(notravel, 1),
        "severe_miles": round(severe, 1),
        "high_miles": round(high, 1),
        "avg_score": round(avg, 2),
        "distance_miles": round(total_mi, 1),
        "duration_hours": round(duration_s / 3600, 2),
    }


def _pick_best(routes):
    def key(r):
        s = r["summary"]
        return (
            s["no_travel_miles"],
            s["severe_miles"],
            s["high_miles"],
            s["avg_score"],
            s["duration_hours"],
        )
    return min(routes, key=key)["index"]


def _build_corridor(cps, wx, departure, load_lb, hours=CORRIDOR_HOURS):
    base = departure.replace(minute=0, second=0, microsecond=0)
    points = []
    for i, cp in enumerate(cps):
        w = wx[i]
        start = weather_mod.index_for_time(w["time"], base)
        risk, wind, rain, snow = [], [], [], []
        last = len(w["time"]) - 1
        for h in range(hours + 1):
            j = min(start + h, last)
            ws = w["wind"][j] or 0.0
            rn = w["rain"][j] or 0.0
            sn = w["snow"][j] or 0.0
            risk.append(checkpoint_risk(ws, rn, sn, load_lb)["score"])
            wind.append(round(ws, 1))
            rain.append(round(rn, 3))
            snow.append(round(sn, 3))
        points.append({
            "lat": round(cp["lat"], 5),
            "lon": round(cp["lon"], 5),
            "mile": round(cp["mile"], 1),
            "risk": risk,
            "wind": wind,
            "rain": rain,
            "snow": snow,
        })
    return {"base_time": base.isoformat(), "hours": hours, "points": points}
