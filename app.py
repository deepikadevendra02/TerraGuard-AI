from pathlib import Path
from flask import Flask, render_template, request, jsonify
from risk_engine import assess_risk, load_demo_data

app = Flask(__name__)
BASE = Path(__file__).resolve().parent

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({"status":"ok","project":"TerraGuard AI","mode":"demonstration"})

@app.get("/api/sites")
def sites():
    rows = load_demo_data(BASE / "data" / "demo_sites.csv")
    results = [assess_risk(r) for r in rows]
    return jsonify({"mode":"synthetic_demo_data","count":len(results),"sites":results})

@app.post("/api/assess")
def assess():
    payload = request.get_json(silent=True) or {}
    required = ["rainfall_mm_24h","slope_deg","soil_saturation_pct","landslide_history"]
    missing = [k for k in required if k not in payload]
    if missing:
        return jsonify({"error":"Missing fields","fields":missing}), 400
    try:
        result = assess_risk(payload)
    except (TypeError, ValueError) as exc:
        return jsonify({"error":str(exc)}), 400
    return jsonify(result)

@app.get("/api/data-sources")
def data_sources():
    return jsonify([
      {"name":"Geological Survey of India (GSI)","role":"Landslide inventory and susceptibility references","url":"https://www.gsi.gov.in/"},
      {"name":"NASA Global Landslide Catalog","role":"Historical event records","url":"https://landslides.nasa.gov/"},
      {"name":"SRTM / NASADEM","role":"Elevation and terrain derivatives","url":"https://lpdaac.usgs.gov/"},
      {"name":"NASA GPM IMERG","role":"Satellite precipitation estimates","url":"https://gpm.nasa.gov/data/imerg"}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT",5000)), debug=False)
