export default function RouteSummary({ routes, selected, onSelect }) {
  return (
    <div className="summaries">
      <h2>Routes</h2>
      {routes.map((r) => {
        const s = r.summary
        const active = r.index === selected
        return (
          <button
            key={r.index}
            type="button"
            className={'route-card' + (active ? ' active' : '')}
            onClick={() => onSelect(r.index)}
          >
            <div className="route-card-head">
              <span>Route {r.index + 1}</span>
              {r.recommended && <span className="badge">Recommended</span>}
            </div>

            <div className="route-stats">
              <span>{s.distance_miles} mi</span>
              <span>{s.duration_hours} h</span>
            </div>

            <div className="route-risk">
              {s.no_travel_miles > 0 && (
                <span className="pill notravel">{s.no_travel_miles} mi no-travel</span>
              )}
              <span className="pill severe">{s.severe_miles} mi severe</span>
              <span className="pill high">{s.high_miles} mi high</span>
              <span className="pill muted">avg risk {s.avg_score}</span>
            </div>
          </button>
        )
      })}
    </div>
  )
}
