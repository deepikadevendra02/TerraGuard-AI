# TerraGuard AI — Landslide Early Warning & Risk Monitoring

**SIH 2026 problem reference:** SIH26001 (as supplied in the problem statement image)

TerraGuard AI is an academic proof-of-concept for screening landslide-prone slopes using rainfall, slope angle, soil saturation, historical landslide evidence, land-cover disturbance and seismicity context. It provides a transparent weighted index, risk band and suggested response actions through a Flask dashboard and JSON API.

> **Critical limitation:** This repository currently runs on synthetic demonstration records and an illustrative weighted scoring model. It is not a trained or calibrated landslide prediction model, does not calculate a true probability of failure, and must never be used for real evacuation or public warnings.

## Features
- Responsive dashboard with six demonstration slope scenarios.
- Interactive site assessment and JSON endpoints.
- Input validation and transparent indicator weights.
- Four screening bands: LOW, MODERATE, HIGH, VERY HIGH.
- Suggested inspection / escalation actions.
- Data-source plan for GSI, NASA Global Landslide Catalog, SRTM/NASADEM and NASA GPM IMERG.
- Unit tests and Render deployment configuration.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## API
- `GET /api/health`
- `GET /api/sites`
- `GET /api/data-sources`
- `POST /api/assess` with JSON:
```json
{
  "site_id":"TEST-01",
  "rainfall_mm_24h":120,
  "slope_deg":32,
  "soil_saturation_pct":70,
  "landslide_history":1,
  "land_cover_disturbance":0.5,
  "seismicity":0.2
}
```

## Test
```bash
python -m unittest discover -s tests -v
```

## Deploy (Render)
1. Push this repository to GitHub.
2. In Render, choose **New → Web Service** and connect the GitHub repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Deploy. Render assigns a public URL after a successful build.

`render.yaml` and `Procfile` are included. Do not commit secrets or private datasets.

## Data integration roadmap
| Input | Intended source | Processing |
|---|---|---|
| Historical landslides | GSI inventory; NASA Global Landslide Catalog | Clean event locations, dates, trigger and inventory quality |
| Terrain | SRTM/NASADEM DEM | Derive slope, aspect, curvature, elevation |
| Rainfall | NASA GPM IMERG; validated IMD/local gauges | Accumulations over 1h/24h/3d/7d; local thresholds |
| Land cover | Appropriate public satellite products | Vegetation / disturbance indicators |
| Soil / geology | GSI and authoritative geospatial layers | Lithology, soil class, drainage and uncertainty |

## Model development before operational use
Acquire geographically representative, quality-controlled labelled events and non-events; prevent spatial/temporal leakage; split by region and time; compare logistic regression, Random Forest and gradient boosting; report precision, recall, F1, PR-AUC, calibration and lead-time performance; calibrate rainfall thresholds locally; validate with domain experts and district authorities.

## Repository structure
```text
TerraGuard-AI/
├── app.py
├── risk_engine.py
├── data/demo_sites.csv
├── templates/index.html
├── static/{style.css,app.js}
├── tests/test_risk_engine.py
├── requirements.txt
├── Procfile
├── render.yaml
└── README.md
```
