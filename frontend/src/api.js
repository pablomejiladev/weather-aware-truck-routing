// In production the API is served from the same origin (empty string).
// For local dev, set VITE_API_URL=http://localhost:8000 in frontend/.env.
const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function planTrip(payload) {
  const res = await fetch(`${BASE}/api/plan/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    throw new Error(data.error || `Request failed (${res.status})`)
  }
  return data
}
