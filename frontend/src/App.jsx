import { useState } from 'react'
import TripForm from './components/TripForm'
import RouteMap from './components/RouteMap'
import RouteSummary from './components/RouteSummary'
import Legend from './components/Legend'
import { planTrip } from './api'

export default function App() {
  const [result, setResult] = useState(null)
  const [selected, setSelected] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(payload) {
    setLoading(true)
    setError(null)
    try {
      const data = await planTrip(payload)
      setResult(data)
      setSelected(data.recommended_index)
    } catch (e) {
      setError(e.message)
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <h1>Weather-Aware Truck Routing</h1>
        <p className="subtitle">Pick the safest route for the weather, load, and timing.</p>

        <TripForm onSubmit={handleSubmit} loading={loading} />
        {error && <div className="error">{error}</div>}

        {result && (
          <RouteSummary
            routes={result.routes}
            selected={selected}
            onSelect={setSelected}
          />
        )}

        <Legend />
      </aside>

      <main className="map-area">
        {result ? (
          <RouteMap result={result} selected={selected} />
        ) : (
          <div className="placeholder">
            {loading ? 'Planning your route…' : 'Enter a trip to see routes, checkpoints, and weather risk.'}
          </div>
        )}
      </main>
    </div>
  )
}
