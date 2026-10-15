export default function ForecastSlider({ hour, onChange, baseTime, max }) {
  const when = new Date(new Date(baseTime).getTime() + hour * 3600 * 1000)
  return (
    <div className="slider">
      <span className="slider-label">Forecast</span>
      <input
        type="range"
        min="0"
        max={max}
        value={hour}
        onChange={(e) => onChange(Number(e.target.value))}
      />
      <span className="slider-value">
        +{hour}h · {when.toLocaleString([], { weekday: 'short', hour: 'numeric' })}
      </span>
    </div>
  )
}
