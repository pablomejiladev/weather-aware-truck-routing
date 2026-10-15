import requests

NOMINATIM = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "weather-aware-truck-routing/1.0 (assessment demo)"}


def geocode(query):
    resp = requests.get(
        NOMINATIM,
        params={"q": query, "format": "json", "limit": 1},
        headers=HEADERS,
        timeout=15,
    )
    resp.raise_for_status()
    results = resp.json()
    if not results:
        raise ValueError(f"Could not find a location for '{query}'.")

    top = results[0]
    return {
        "label": top["display_name"],
        "lat": float(top["lat"]),
        "lon": float(top["lon"]),
    }
