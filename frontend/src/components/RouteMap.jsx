import { useEffect, useState } from 'react'
import {
  MapContainer,
  TileLayer,
  Polyline,
  CircleMarker,
  Popup,
  useMap,
} from 'react-leaflet'
import L from 'leaflet'
import 'leaflet.heat'
import { scoreColor } from '../risk'
import ForecastSlider from './ForecastSlider'

// Draws the leaflet.heat layer for the selected forecast hour.
function HeatLayer({ points, hour }) {
  const map = useMap()
  useEffect(() => {
    const data = points
      .map((p) => [p.lat, p.lon, (p.risk[hour] ?? 0) / 4])
      .filter((d) => d[2] > 0)

    const layer = L.heatLayer(data, {
      radius: 35,
      blur: 25,
      minOpacity: 0.3,
      max: 1,
      gradient: {
        0.0: '#2e9e5b',
        0.3: '#f2c200',
        0.55: '#f08a00',
        0.8: '#e23b2e',
        1.0: '#6a1b9a',
      },
    })
    layer.addTo(map)
    return () => map.removeLayer(layer)
  }, [map, points, hour])

  return null
}

function FitBounds({ geometry }) {
  const map = useMap()
  useEffect(() => {
    const latlngs = geometry.map((c) => [c[1], c[0]])
    if (latlngs.length) map.fitBounds(latlngs, { padding: [40, 40] })
  }, [map, geometry])
  return null
}

export default function RouteMap({ result, selected }) {
  const [hour, setHour] = useState(0)
  const [showHeat, setShowHeat] = useState(true)

  const routes = result.routes
  const active = routes[selected]
  const center = [result.origin.lat, result.origin.lon]

  return (
    <div className="map-wrap">
      <div className="map-controls">
        <label className="toggle">
          <input
            type="checkbox"
            checked={showHeat}
            onChange={(e) => setShowHeat(e.target.checked)}
          />
          Weather heatmap
        </label>
        <ForecastSlider
          hour={hour}
          onChange={setHour}
          baseTime={result.corridor.base_time}
          max={result.corridor.hours}
        />
      </div>

      <MapContainer center={center} zoom={6} className="leaflet-map" scrollWheelZoom>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        <FitBounds geometry={active.geometry} />

        {routes.map((r) => (
          <Polyline
            key={r.index}
            positions={r.geometry.map((c) => [c[1], c[0]])}
            pathOptions={{
              color: r.index === selected ? '#1d4ed8' : '#9aa5b1',
              weight: r.index === selected ? 6 : 3,
              opacity: r.index === selected ? 0.9 : 0.5,
            }}
          />
        ))}

        {active.checkpoints.map((cp, i) => (
          <CircleMarker
            key={i}
            center={[cp.lat, cp.lon]}
            radius={6}
            pathOptions={{
              color: '#1a1a1a',
              weight: 1,
              fillColor: scoreColor(cp.score),
              fillOpacity: 0.95,
            }}
          >
            <Popup>
              <b>Mile {cp.mile}</b> — <b>{cp.risk}</b>
              <br />
              ETA {new Date(cp.eta).toLocaleString()}
              <br />
              Wind {cp.wind} mph ({cp.wind_level})
              <br />
              Rain {cp.rain} in/hr ({cp.rain_level})
              <br />
              Snow {cp.snow} in/hr ({cp.snow_level})
            </Popup>
          </CircleMarker>
        ))}

        {showHeat && <HeatLayer points={result.corridor.points} hour={hour} />}
      </MapContainer>
    </div>
  )
}
