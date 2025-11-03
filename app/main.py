from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import telex_webhook, cultural_agent
from app.config import logger

app = FastAPI(
    title="Telex Cultural Coworker API",
    description="An AI Agent that provides real-time cultural insights and assistance via the A2A Protocol.",
    version="1.0.0"
)

# --- CORS Middleware (safe for Railway / Telex.im API calls) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later if you get a frontend or secure Telex domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routers ---
app.include_router(telex_webhook.router, prefix="/api/v1", tags=["Telex Webhook"])
app.include_router(cultural_agent.router, prefix="/api/v1", tags=["Cultural Insights"])

# --- Health Check Endpoint ---
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint to verify API status."""
    logger.info("Health check called - API is running.")
    return {
        "status": "healthy",
        "message": "Telex Cultural Coworker API is running smoothly.",
        "version": "1.0.0"
    }
