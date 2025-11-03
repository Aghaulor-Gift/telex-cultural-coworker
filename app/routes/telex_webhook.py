from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.services.gemini_service import get_cultural_insights
from app.config import logger, AGENT_ID, AGENT_NAME, AGENT_DESCRIPTION, AGENT_DOMAIN
from app.models.schemas import A2ARequest
from datetime import datetime

router = APIRouter()
A2A_WEBHOOK_PATH = "/a2a/telex-cultural"

# --- 1. AGENT CARD ENDPOINT ---
@router.get("/.well-known/agent.json", include_in_schema=False)
def get_agent_card():
    """Serves the Agent-to-Agent (A2A) definition for Telex."""
    logger.info(f"Serving Agent Card for ID: {AGENT_ID}")

    webhook_url = f"{AGENT_DOMAIN}{A2A_WEBHOOK_PATH}"

    agent_card = {
        "id": AGENT_ID,
        "name": AGENT_NAME,
        "description": AGENT_DESCRIPTION,
        "schemaVersion": "0.1.0",
        "methods": [
            {
                "name": "cultural_insights",
                "description": "Retrieves real-time cultural, etiquette, and trend insights for a specific location.",
                "parameters": {
                    "location": {
                        "type": "string",
                        "description": "The city or country to get insights for (e.g., 'Tokyo', 'Brazil')."
                    }
                },
                "response": {
                    "type": "object",
                    "properties": {
                        "insights": {
                            "type": "string",
                            "description": "Markdown or structured JSON text with cultural summary, cuisine, and travel recommendations."
                        }
                    }
                },
                "url": "hhtps://telex-cultural-coworker-production.up.railway.app/a2a/telex-cultural",
            }
        ],
        "defaultMethod": "cultural_insights"
    }

    return JSONResponse(content=agent_card)


# --- 2. MAIN A2A WEBHOOK ENDPOINT ---
@router.post(A2A_WEBHOOK_PATH, include_in_schema=False)
async def telex_webhook(request: A2ARequest):
    """
    Handles A2A JSON-RPC 'invoke' requests from Telex.im and returns
    structured, AI-enhanced cultural insights.
    """
    try:
        if request.method != "cultural_insights":
            raise ValueError("Unsupported method. Must be 'cultural_insights'.")

        location = getattr(request.data, "location", None)
        if not location:
            raise ValueError("Missing 'location' parameter in data payload.")

        logger.info(f"Received A2A request for location: {location}")

        # --- Default Base Insights ---
        insights = {
            "culture": f"{location} has a rich cultural identity emphasizing respect, tradition, and community harmony.",
            "communication_style": f"People in {location} communicate politely and prefer indirect expression to maintain harmony.",
            "business_etiquette": f"In {location}, punctuality, formality, and respect for hierarchy are vital in business settings.",
            "food_and_cuisine": f"{location}'s cuisine is diverse, flavorful, and often tied to seasonal and regional ingredients.",
            "lifestyle_and_customs": f"The lifestyle in {location} balances work, family, and leisure with an emphasis on social unity.",
            "dress_code": f"Typical dress in {location} reflects modesty and professionalism, depending on the occasion.",
            "marketing_tips": f"To market effectively in {location}, emphasize authenticity, community values, and cultural respect.",
            "travel_recommendations": f"Explore popular landmarks and cultural districts in {location} to understand its living heritage.",
            "festivals_and_celebrations": f"{location} hosts colorful festivals that showcase its history, music, and culinary traditions."
        }

        # --- Gemini AI Enrichment ---
        try:
            ai_generated = await get_cultural_insights(location)
            if isinstance(ai_generated, dict):
                insights.update(ai_generated)
        except Exception as ai_err:
            logger.warning(f"Gemini API unavailable or failed: {ai_err}")

        # --- Full Telex Agent Response ---
        response_payload = {
            "active": True,
            "category": "Cultural Insights and Marketing",
            "description": "A workflow for retrieving AI-generated cultural insights for global markets.",
            "id": AGENT_ID,
            "name": AGENT_NAME,
            "short_description": "An AI agent that delivers cultural insights for global engagement.",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "response": {
                "status": "success",
                "location": location,
                "insights": insights
            },
        }

        logger.info(f"Successfully generated insights for: {location}")
        return JSONResponse(content=response_payload, status_code=status.HTTP_200_OK)

    except ValueError as ve:
        logger.warning(f"A2A Request Validation Error: {ve}")
        return JSONResponse(
            content={"error": str(ve)},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        logger.error(f"A2A Webhook Internal Error: {e}")
        return JSONResponse(
            content={"error": "Internal Server Error during insight generation."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
