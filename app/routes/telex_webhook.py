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
    """Serve the Agent-to-Agent (A2A) protocol agent definition."""
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
                "description": "Retrieves cultural, etiquette, and trend insights for a specific location.",
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
                            "description": "Markdown text with cultural summary, food, and travel tips."
                        }
                    }
                },
                "url": webhook_url,
            }
        ],
        "defaultMethod": "cultural_insights"
    }
    return JSONResponse(content=agent_card)


# --- 2. MAIN WEBHOOK ENDPOINT ---
@router.post(A2A_WEBHOOK_PATH, include_in_schema=False)
async def telex_webhook(request: A2ARequest):
    """Handle A2A JSON-RPC 'invoke' requests and return structured cultural insights."""
    try:
        if request.method != "cultural_insights":
            raise ValueError("Unsupported method: Must be 'cultural_insights'")

        location = getattr(request.data, "location", None)
        if not location:
            raise ValueError("Missing 'location' parameter in data payload.")

        logger.info(f"Received A2A invocation for location: {location}")

        # Base cultural insights
        insights = {
            "culture": f"{location} has a unique cultural identity that values respect, tradition, and social harmony.",
            "communication_style": f"People in {location} tend to communicate politely and contextually, avoiding confrontation.",
            "business_etiquette": f"In {location}, punctuality, hierarchy, and formal greetings are important in business interactions.",
            "food_and_cuisine": f"{location}'s cuisine is diverse and flavorful, often centered around fresh, local ingredients.",
            "lifestyle_and_customs": f"The lifestyle in {location} balances work, family, and social gatherings, emphasizing community and tradition.",
            "dress_code": f"Dress codes in {location} are typically modest and occasion-appropriate, showing respect for others.",
            "marketing_tips": f"When marketing in {location}, focus on trust, cultural authenticity, and community-driven storytelling.",
            "travel_recommendations": f"Explore popular landmarks and festivals in {location} to experience local culture firsthand.",
            "festivals_and_celebrations": f"{location} celebrates various festivals that reflect its history, religion, and regional diversity."
        }

        # --- Integrate Gemini AI output ---
        try:
            ai_extra = await get_cultural_insights(location)
            if isinstance(ai_extra, dict):
                insights.update(ai_extra)
        except Exception as ai_err:
            logger.warning(f"Gemini service unavailable: {ai_err}")

        # --- Response Payload ---
        return {
            "active": True,
            "category": "Cultural Insights and Marketing",
            "description": "A workflow for retrieving AI-generated cultural insights for global markets.",
            "id": AGENT_ID,
            "name": "Telex Cultural Coworker",
            "short_description": "An AI agent that delivers cultural insights for global engagement.",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "response": {
                "status": "success",
                "location": location,
                "insights": insights
            }
        }

    except ValueError as ve:
        logger.warning(f"A2A Request Validation Error: {ve}")
        return JSONResponse(content={"error": str(ve)}, status_code=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"A2A Webhook Internal Error: {e}")
        return JSONResponse(
            content={"error": "Internal Server Error during insight generation."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
