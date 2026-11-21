# HarvestIQ

HarvestIQ is a prototype agriculture and market-intelligence web application focused on Tamil Nadu. It combines a single-page dashboard with a FastAPI backend to demonstrate crop matching, mandi prices, selling decisions, weather information, government schemes, and district-level analytics.

> **Prototype notice:** Recommendations, forecasts, market prices, weather alerts, scheme details, and district metrics may be seeded, simulated, or otherwise illustrative. Verify current information with official sources before making financial, agricultural, or eligibility decisions.

## Features

- **Soil and crop matching:** Enter soil nutrient and pH values to view crop suitability and estimated costs, yields, and returns. Includes sample soil health cards and a mock upload flow.
- **Mandi prices and selling guidance:** Browse crop and district price records, compare selling now versus waiting, and estimate net returns from nearby markets.
- **Forecasts, weather, and schemes:** Explore price trend visualizations, district weather information, and national and Tamil Nadu scheme guides.
- **District analytics:** View Tamil Nadu district metrics and adjust procurement assumptions in a what-if simulator.
- **Accessibility and languages:** The interface includes multilingual labels and browser-based voice input and read-aloud controls.

## Requirements

- Python 3.10 or later
- pip

## Run locally

From the repository root, create and activate a virtual environment, install the backend dependencies, and start the application:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python -m backend.main
```

If PowerShell prevents activation, you can invoke the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\.venv\Scripts\python.exe -m backend.main
```

Then open:

- Web application: <http://localhost:8000/>
- Interactive API documentation: <http://localhost:8000/docs>

The backend initializes its SQLite database and reloads sample price and dashboard records on startup. The frontend is served by the FastAPI application from `frontend/index.html`.

## Deploy to Render

The repository includes a Render Blueprint in `render.yaml`. In Render, choose **New + → Blueprint**, connect this GitHub repository, and approve creation of the `harvest-iq` web service. Render will install `backend/requirements.txt`, start the FastAPI app, and use `/` for its health check.

The Blueprint uses Render's free plan. Its filesystem is ephemeral, so local SQLite data and submitted feedback are not durable across restarts or redeploys; the app reloads its sample records at startup.

## API endpoints

The API is mounted at `/api`. Interactive request and response schemas are available at `/docs`.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/prices` | List mandi prices |
| `GET` | `/api/soil-health-card/{card_no}` | Retrieve a sample soil health card |
| `POST` | `/api/soil-health-card/upload-mock` | Demonstrate the mock card-upload flow |
| `POST` | `/api/soil-analysis` | Analyze soil and recommend crops |
| `POST` | `/api/sell-decision` | Generate a sell-or-wait estimate |
| `POST` | `/api/best-market` | Compare market options |
| `GET` | `/api/forecast/{crop}` | Retrieve a crop price forecast |
| `GET` | `/api/schemes` | List scheme information |
| `GET` | `/api/weather/{district}` | Retrieve district weather information |
| `GET` | `/api/govtech/overview` | Retrieve district analytics |
| `GET` | `/api/govtech/simulate` | Simulate procurement scenarios |
| `POST` | `/api/feedback` | Submit recommendation feedback |

## Project layout

```text
backend/       FastAPI app, API routes, and SQLite persistence
frontend/      Single-page web interface
```

## Data and verification

The application is intended for demonstration and development. Confirm the source, date, and accuracy of any data displayed in the dashboard. Do not rely on prototype outputs as official market quotations, forecasts, weather warnings, or government guidance.
