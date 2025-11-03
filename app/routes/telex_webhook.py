from fastapi import APIRouter, Request, HTTPException
from app.services.gemini_service import get_cultural_insights
from app.config import logger

router = APIRouter()

@router.post("/telex")
async def telex_webhook(request: Request):
    """Handle Telex webhook requests."""
    try:
        body = await request.json()
        location = body.get("data", {}).get("location")

        if not location:
            raise HTTPException(status_code=400, detail="Missing 'location' in data")

        logger.info(f"Received Telex query for: {location}")

        insights = get_cultural_insights(location)
        return {
            "status": "success",
            "response": {
                "location": location,
                "insights": insights
            }
        }

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))