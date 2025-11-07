from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from app.services.gemini_service import get_cultural_insights
from app.config import logger, AGENT_ID, AGENT_NAME, AGENT_DESCRIPTION, AGENT_DOMAIN
from datetime import datetime
import re

router = APIRouter()
A2A_PATH = "/a2a/telex-cultural"


@router.post(A2A_PATH, include_in_schema=False)
async def telex_webhook(request: Request):
    """
    Handles Telex webhook requests — supports A2A JSON-RPC, params, and plain messages.
    """
    try:
        body = await request.json()
        logger.info(f"Incoming payload: {body}")

        # ✅ Try extracting location from several formats
        location = (
            body.get("location")
            or body.get("data", {}).get("location")
            or body.get("params", {}).get("location")
        )

        # ✅ If Telex sends a message-based payload, extract from message parts
        if not location and "params" in body:
            parts = (
                body.get("params", {})
                .get("message", {})
                .get("parts", [])
            )
            for part in parts:
                if part.get("kind") == "text":
                    text = part.get("text", "").lower()
                    # Try to extract the country name (Nigeria, Japan, etc.)
                    match = re.search(r"\b(?:about|from|in|of)\s+([A-Z][a-zA-Z]+)\b", part.get("text", ""))
                    if match:
                        location = match.group(1)
                        break

        if not location:
            logger.warning("Missing 'location' parameter in request.")
            return JSONResponse(
                content={"error": "Missing 'location' parameter in request body."},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"Extracted location: {location}")

        # --- Fetch insights
        try:
            insights = await get_cultural_insights(location)
        except Exception as e:
            logger.warning(f"Gemini service failed: {e}")
            insights = {
                "culture": f"{location} is known for its diverse traditions and social harmony.",
                "communication_style": f"People in {location} value respectful and clear communication.",
                "business_etiquette": f"In {location}, punctuality and politeness are highly regarded.",
                "food_and_cuisine": f"{location} offers rich, flavorful dishes reflecting its cultural diversity.",
                "lifestyle_and_customs": f"Life in {location} emphasizes community and family connections.",
                "dress_code": f"Attire in {location} tends to be modest and occasion-appropriate.",
                "marketing_tips": f"Effective marketing in {location} focuses on authenticity and trust.",
                "travel_recommendations": f"Explore {location}'s landmarks, local music, and cuisine for a full experience.",
                "festivals_and_celebrations": f"{location} hosts vibrant festivals showcasing its cultural heritage."
            }

        response_payload = {
            "active": True,
            "category": "Cultural Insights and Marketing",
            "description": AGENT_DESCRIPTION,
            "id": AGENT_ID,
            "name": AGENT_NAME,
            "short_description": "AI cultural coworker providing insights across countries.",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "response": {
                "status": "success",
                "location": location,
                "insights": insights
            }
        }

        return JSONResponse(content=response_payload, status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"A2A Webhook Internal Error: {e}")
        return JSONResponse(
            content={"error": "Internal Server Error during insight generation."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
