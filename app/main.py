from fastapi import FastAPI
from app.routes import telex_webhook, cultural_agent

app = FastAPI(
    title="Telex Cultural Coworker API",
    description="An AI Agent that provides real-time cultural insights and assistance via the A2A Protocol.",
    version="1.0.0"
)



# Include Routers
app.include_router(telex_webhook.router, prefix="/api/v1", tags=["Telex Webhook"])
app.include_router(cultural_agent.router, prefix="/api/v1", tags=["Cultural Insights"])

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint to verify API status."""
    return {
        "status": "healthy",
        "message": "Telex Cultural Coworker API is running smoothly",
        "version": "1.0.0"
    }
