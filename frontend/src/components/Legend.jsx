import { RISK_LEVELS, RISK_COLORS } from '../risk'

export default function Legend() {
  return (
    <div className="legend">
      <h3>Risk levels</h3>
      {RISK_LEVELS.map((lvl) => (
        <div key={lvl} className="legend-row">
          <span className="swatch" style={{ background: RISK_COLORS[lvl] }} />
          {lvl}
        </div>
      ))}
    </div>
  )
}
