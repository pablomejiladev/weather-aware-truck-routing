import requests

OSRM = "https://router.project-osrm.org/route/v1/driving"


def get_routes(origin, destination, max_routes=3):
    coords = f"{origin['lon']},{origin['lat']};{destination['lon']},{destination['lat']}"
    resp = requests.get(
        f"{OSRM}/{coords}",
        params={
            "alternatives": max_routes,
            "overview": "full",
            "geometries": "geojson",
        },
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != "Ok":
        raise ValueError("Routing failed: " + data.get("message", data.get("code", "unknown")))

    routes = []
    for i, r in enumerate(data["routes"][:max_routes]):
        routes.append({
            "index": i,
            "distance_m": r["distance"],
            "duration_s": r["duration"],
            "geometry": r["geometry"]["coordinates"],  # [[lon, lat], ...]
        })
    return routes
