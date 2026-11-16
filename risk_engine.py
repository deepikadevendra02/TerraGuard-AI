"""Transparent, rule-based landslide screening score for a classroom prototype.

This is NOT a calibrated probability of failure or an operational warning system.
Weights and thresholds are illustrative and must be calibrated against local
inventory, rainfall, geotechnical and terrain observations before real use.
"""
from pathlib import Path
import csv

WEIGHTS = {
    "rainfall": 0.30, "slope": 0.20, "soil_saturation": 0.20,
    "landslide_history": 0.15, "land_cover_disturbance": 0.10, "seismicity": 0.05
}

def _number(data, key, low, high):
    try: value = float(data[key])
    except (KeyError, TypeError, ValueError): raise ValueError(f"{key} must be numeric")
    if not low <= value <= high: raise ValueError(f"{key} must be between {low} and {high}")
    return value

def assess_risk(data):
    rain = _number(data, "rainfall_mm_24h", 0, 1000)
    slope = _number(data, "slope_deg", 0, 90)
    saturation = _number(data, "soil_saturation_pct", 0, 100)
    history = _number(data, "landslide_history", 0, 1)
    disturbance = _number(data, "land_cover_disturbance", 0, 1) if "land_cover_disturbance" in data else 0.5
    seismic = _number(data, "seismicity", 0, 1) if "seismicity" in data else 0.0

    # Convert heterogeneous inputs to transparent 0–100 indicators.
    indicators = {
      "rainfall": min(rain / 200 * 100, 100),
      "slope": min(slope / 45 * 100, 100),
      "soil_saturation": saturation,
      "landslide_history": history * 100,
      "land_cover_disturbance": disturbance * 100,
      "seismicity": seismic * 100
    }
    score = round(sum(indicators[k] * WEIGHTS[k] for k in WEIGHTS), 1)
    level = "LOW" if score < 30 else "MODERATE" if score < 55 else "HIGH" if score < 75 else "VERY HIGH"
    actions = {
      "LOW":["Continue routine slope and drainage inspections.","Maintain vegetation and keep drainage channels clear."],
      "MODERATE":["Increase observation during intense or prolonged rainfall.","Inspect cracks, seepage, retaining structures and blocked drains."],
      "HIGH":["Notify local disaster-management personnel for field verification.","Restrict access to visibly unstable slopes and prepare evacuation communication."],
      "VERY HIGH":["Treat as an urgent screening alert and request immediate expert assessment.","Follow official district/SDMA instructions; move people only under authorized evacuation guidance."]
    }[level]
    return {
      "site_id": str(data.get("site_id","USER-INPUT")),
      "risk_score": score, "risk_level": level,
      "indicator_scores": indicators, "weights": WEIGHTS,
      "recommended_actions": actions,
      "disclaimer":"Screening prototype only. Not a validated forecast, probability, or substitute for official warnings."
    }

def load_demo_data(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
