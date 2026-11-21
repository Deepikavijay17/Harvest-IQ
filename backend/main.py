import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from . import database, routes

app = FastAPI(
    title="HarvestIQ — Tamil Nadu Agriculture & Market Intelligence Engine",
    description="High-performance backend for live Agmarknet mandi tracking, soil-matching, sell decisions, and GovTech analytics.",
    version="1.0.0"
)

# Enable CORS for local Vite and external clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(routes.api_router, prefix="/api", tags=["HarvestIQ API"])

frontend_html = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    if os.path.exists(frontend_html):
        with open(frontend_html, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h2>HarvestIQ API Running. Frontend index.html not found.</h2>")

@app.on_event("startup")
async def startup_event():
    await database.init_db()
    await database.refresh_prices()
    print("HarvestIQ database initialized and seeded with latest Agmarknet data.")

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
