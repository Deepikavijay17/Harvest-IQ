# HarvestIQ Prototype Implementation Plan

## Goal Description
Create a simplified prototype for the "HarvestIQ" agriculture and market intelligence platform targeting Tamil Nadu farmers and district officers. The prototype will use a clean architecture with a React + Vite + Tailwind frontend and a FastAPI backend powered by SQLite/mock data. It will include core farmer dashboard features, live mandi price tracker, and basic district dashboard, with multilingual support (5 native languages).

## User Review Required
> [!IMPORTANT] 
> The plan outlines a minimal viable product (MVP) focusing on the live-price backend as the next immediate build step. Please review the proposed folder structure, data sources, and feature scope. Confirm if you want to proceed with this MVP or adjust priorities.

## Open Questions
> [!QUESTION] 
> 1. **Data source URLs**: Do you have a specific Agmarknet open data endpoint you want us to hit for daily prices, or should we use the public API documented here: https://data.gov.in/resources/agmarknet-daily-price-data ?
> 2. **Native language list**: Which five languages should be supported (e.g., Tamil, Telugu, Malayalam, Kannada, English)?
> 3. **Deployment target**: Should the prototype be runnable locally via `npm run dev` and `uvicorn`, or do you need a simple cloud deployment (e.g., Vercel/Render) for demonstration?
> 4. **Authentication**: Do you need any user login/auth, or should the prototype be open for any user?
> 5. **Forecasting model**: For the real price forecasting feature, do you prefer a quick statsmodels SARIMA implementation, or a placeholder that returns static forecast data until a model is trained?

## Proposed Changes
---
### Backend (FastAPI)
- **[NEW] backend/** directory containing the FastAPI app.
- **[NEW] backend/main.py** – entry point, includes routers for `/prices`, `/soil`, `/schemes`.
- **[NEW] backend/models.py** – Pydantic models for request/response schemas.
- **[NEW] backend/database.py** – SQLite connection and mock data utilities.
- **[NEW] backend/price_fetcher.py** – async task to pull daily mandi prices from Agmarknet and store in SQLite.
- **[NEW] backend/forecast.py** – placeholder SARIMA forecasting stub (real model can be swapped later).
- **[NEW] backend/i18n.py** – simple translation dictionary for the five supported languages.

### Frontend (React + Vite)
- **[NEW] frontend/** directory.
- **[NEW] frontend/vite.config.ts** – Vite config.
- **[NEW] frontend/tailwind.config.js** – Tailwind configuration with emerald and earth tone palette.
- **[NEW] frontend/src/App.tsx** – Main app with routing (react-router-dom).
- **[NEW] frontend/src/components/** – UI components:
  - `FarmerDashboard.tsx`
  - `SoilForm.tsx`
  - `MandiPriceTable.tsx`
  - `SchemeChecker.tsx`
  - `DistrictDashboard.tsx`
  - `PriceForecastChart.tsx`
  - `LanguageSwitcher.tsx`
- **[NEW] frontend/src/api.ts** – wrapper around fetch calls to backend.

### Shared Assets
- **[NEW] assets/** – icons, placeholder images, and color palette definitions.

### Multilingual Support
- JSON translation files under **frontend/src/locales/** (e.g., `ta.json`, `en.json`, `kn.json`, `ml.json`, `te.json`).
- Simple `useTranslation` hook that picks language based on user selection.

### Live Mandi Price Backend (First Build Step)
- Implement `/prices` endpoint that returns current prices for the four key crops across districts.
- `price_fetcher.py` runs on server start, fetches data daily, stores in SQLite table `prices`.
- Provide a script (`scripts/fetch_prices.py`) that can be triggered manually for testing.

### Development & Run Scripts
- **[NEW] start.sh** – convenience script to launch both backend (`uvicorn backend.main:app --reload`) and frontend (`npm run dev`).
- **[NEW] README.md** – instructions for setup, running, and testing.

## Verification Plan
### Automated Tests
- Backend unit tests using `pytest` for price fetching, schema validation, and translation lookup.
- Frontend component tests with `@testing-library/react` for rendering key dashboards.

### Manual Verification
- Start the app locally, navigate to Farmer Dashboard, confirm soil form auto‑fills from mock card number.
- Verify Mandi Price Table shows live data pulled from Agmarknet.
- Switch languages and ensure UI updates.
- Check that the price forecast chart displays static placeholder data (to be replaced later).
- Confirm responsive layout on mobile and desktop breakpoints.

---
*Once you approve this plan, I will proceed to scaffold the repository, implement the live‑price backend, and set up the basic frontend pages.*
