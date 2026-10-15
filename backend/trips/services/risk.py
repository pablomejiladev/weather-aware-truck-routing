
LEVELS = ["Low", "Moderate", "High", "Severe", "No Travel"]
LEVEL_INDEX = {name: i for i, name in enumerate(LEVELS)}


def wind_level(mph):
    if mph >= 55:
        return "No Travel"
    if mph >= 45:
        return "Severe"
    if mph >= 35:
        return "High"
    if mph >= 25:
        return "Moderate"
    return "Low"


def rain_level(in_per_hr):
    if in_per_hr > 1.0:
        return "No Travel"
    if in_per_hr > 0.50:
        return "Severe"
    if in_per_hr > 0.25:
        return "High"
    if in_per_hr >= 0.10:
        return "Moderate"
    return "Low"


def snow_level(in_per_hr):
    if in_per_hr > 3.0:
        return "No Travel"
    if in_per_hr > 2.0:
        return "Severe"
    if in_per_hr > 1.0:
        return "High"
    if in_per_hr >= 0.5:
        return "Moderate"
    return "Low"


def _worst(*levels):
    return max(levels, key=lambda lv: LEVEL_INDEX[lv])


def checkpoint_risk(wind, rain, snow, load_lb):
    wind = wind or 0.0
    rain = rain or 0.0
    snow = snow or 0.0

    w = wind_level(wind)
    
    if 45 <= wind <= 54 and load_lb > 30000:
        w = "No Travel"
    elif 35 <= wind <= 44 and load_lb > 40000:
        w = "Severe"

    r = rain_level(rain)
    s = snow_level(snow)
    overall = _worst(w, r, s)

    return {
        "wind_level": w,
        "rain_level": r,
        "snow_level": s,
        "overall": overall,
        "score": LEVEL_INDEX[overall],
    }
