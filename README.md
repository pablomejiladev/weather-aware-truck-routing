---
title: Weather Aware Truck Routing
emoji: 🚚
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Weather-Aware Truck Routing

A React + Django app that helps a truck driver pick the safest route based on
weather, load weight, and timing. The driver enters an origin, destination,
departure time, and load weight; the app generates three route options, samples
the forecast at checkpoints along each one (using the estimated arrival time at
each checkpoint), scores the weather risk, and recommends the safest route.

## Features

- Geocodes origin and destination (OpenStreetMap / Nominatim).
- Generates up to **3 route alternatives** (OSRM).
- Samples weather every **10 / 25 / 50 miles** (selectable) using each
  checkpoint's **estimated arrival time** (Open-Meteo hourly forecast).
- Classifies risk per checkpoint with the Spotter **risk + load rules**.
- Recommends the best route by the required preference order.
- Shows all routes, checkpoints, risk levels, ETAs, and summaries on a map.
- Draws a **weather risk heatmap** along the corridor with a **0–48h slider**.

## Risk logic

Each checkpoint is classified per condition and the **worst** condition wins.

| Condition | Low | Moderate | High | Severe | No Travel |
|-----------|-----|----------|------|--------|-----------|
| Wind (mph) | <25 | 25–34 | 35–44 | 45–54 | ≥55 |
| Rain (in/hr) | <0.10 | 0.10–0.25 | 0.25–0.50 | 0.50–1.00 | >1.00 |
| Snow (in/hr) | <0.5 | 0.5–1.0 | 1.0–2.0 | 2.0–3.0 | >3.0 |

Load rules (applied on top of the wind band):

- ≥55 mph → No Travel for any load
- 45–54 mph + >30,000 lb → No Travel
- 35–44 mph + >40,000 lb → Severe

**Recommendation order:** fewest No-Travel miles → fewest Severe miles →
fewest High miles → lowest average risk → shortest travel time.

## Project layout

```
backend/    Django + DRF API (geocode, routing, weather, risk, planner)
frontend/   React + Vite + Leaflet UI (form, map, heatmap, slider)
Dockerfile  Builds the frontend and serves everything from Django on port 7860
```

## Running locally

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
cp .env.example .env
python manage.py runserver
```

Frontend:

```bash
cd frontend
npm install
cp .env.example .env           # sets VITE_API_URL=http://localhost:8000
npm run dev
```

Run the backend tests with `python manage.py test`.

## API

`POST /api/plan/`

```json
{
  "origin": "Denver, CO",
  "destination": "Salt Lake City, UT",
  "departure": "2026-10-15T08:00:00Z",
  "load_lb": 42000,
  "interval_miles": 25
}
```

Returns the routes (geometry, checkpoints, risk levels, ETAs, summaries), the
recommended route index, and a corridor forecast series for the heatmap.

## Third-party services (all free, keyless)

- **Nominatim** (OpenStreetMap) — geocoding
- **OSRM** demo server — routing with alternatives
- **Open-Meteo** — hourly wind / rain / snow forecast

## Deployment (Hugging Face Spaces, Docker)

The `Dockerfile` builds the React app and serves it together with the Django
API from one container on port 7860. Set a `SECRET_KEY` secret on the Space.
