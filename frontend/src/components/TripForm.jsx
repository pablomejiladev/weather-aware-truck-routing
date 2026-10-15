import { useState } from 'react'

function defaultDeparture() {
  const t = new Date(Date.now() + 60 * 60 * 1000)
  t.setMinutes(0, 0, 0)
  // Format as a local datetime-local value (YYYY-MM-DDTHH:mm).
  const pad = (n) => String(n).padStart(2, '0')
  return `${t.getFullYear()}-${pad(t.getMonth() + 1)}-${pad(t.getDate())}T${pad(t.getHours())}:${pad(t.getMinutes())}`
}

export default function TripForm({ onSubmit, loading }) {
  const [origin, setOrigin] = useState('Denver, CO')
  const [destination, setDestination] = useState('Salt Lake City, UT')
  const [departure, setDeparture] = useState(defaultDeparture)
  const [loadLb, setLoadLb] = useState(42000)
  const [interval, setIntervalMiles] = useState(25)

  function submit(e) {
    e.preventDefault()
    onSubmit({
      origin,
      destination,
      departure: new Date(departure).toISOString(),
      load_lb: Number(loadLb),
      interval_miles: Number(interval),
    })
  }

  return (
    <form className="trip-form" onSubmit={submit}>
      <label>
        Origin
        <input value={origin} onChange={(e) => setOrigin(e.target.value)} required />
      </label>

      <label>
        Destination
        <input value={destination} onChange={(e) => setDestination(e.target.value)} required />
      </label>

      <label>
        Departure
        <input
          type="datetime-local"
          value={departure}
          onChange={(e) => setDeparture(e.target.value)}
          required
        />
      </label>

      <div className="field-row">
        <label>
          Load weight (lb)
          <input
            type="number"
            min="0"
            step="500"
            value={loadLb}
            onChange={(e) => setLoadLb(e.target.value)}
            required
          />
        </label>

        <label>
          Sample every
          <select value={interval} onChange={(e) => setIntervalMiles(e.target.value)}>
            <option value="10">10 miles</option>
            <option value="25">25 miles</option>
            <option value="50">50 miles</option>
          </select>
        </label>
      </div>

      <button type="submit" disabled={loading}>
        {loading ? 'Planning…' : 'Plan route'}
      </button>
    </form>
  )
}
