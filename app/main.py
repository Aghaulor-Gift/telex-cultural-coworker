from fastapi import FastAPI
from app.routes import cultural_agent, telex_webhook

app = FastAPI(title="Telex Cultural Coworker API")

app.include_router(telex_webhook.router, prefix="/api/v1", tags=["Telex Webhook"])
app.include_router(cultural_agent.router, prefix="/api/v1", tags=["Cultural Insights"])

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "message": "Telex Cultural Coworker API is running smoothly"}