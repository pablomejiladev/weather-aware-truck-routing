export const RISK_LEVELS = ['Low', 'Moderate', 'High', 'Severe', 'No Travel']

export const RISK_COLORS = {
  Low: '#2e9e5b',
  Moderate: '#f2c200',
  High: '#f08a00',
  Severe: '#e23b2e',
  'No Travel': '#6a1b9a',
}

export function scoreColor(score) {
  return RISK_COLORS[RISK_LEVELS[score]] || '#999999'
}
