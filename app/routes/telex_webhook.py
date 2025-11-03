from fastapi import APIRouter, Request, HTTPException
from app.services.gemini_service import get_cultural_insights
from app.config import logger
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

# Load .env if it exists
load_dotenv()

router = APIRouter()

# Generate or load persistent Telex Agent ID
TELEX_AGENT_ID = os.getenv("TELEX_AGENT_ID")
if not TELEX_AGENT_ID:
    TELEX_AGENT_ID = str(uuid.uuid4())
    with open(".env", "a") as env_file:
        env_file.write(f"\nTELEX_AGENT_ID={TELEX_AGENT_ID}")
    logger.info(f"Generated new Telex Agent ID: {TELEX_AGENT_ID}")
else:
    logger.info(f"Using existing Telex Agent ID: {TELEX_AGENT_ID}")


@router.post("/a2a/telex-cultural")
async def telex_webhook(request: Request):
    """Handle Telex webhook requests and return structured cultural insights."""
    try:
        body = await request.json()
        location = body.get("data", {}).get("location")

        if not location:
            raise HTTPException(status_code=400, detail="Missing 'location' in data")

        logger.info(f"Received Telex query for: {location}")

        # --- Enhanced structured insights ---
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

        # --- Full Telex Agent payload ---
        return {
            "active": True,
            "category": "Cultural Insights and Marketing",
            "description": "A workflow for retrieving AI-generated cultural insights for global markets.",
            "id": TELEX_AGENT_ID,
            "long_description": (
                "The Telex Cultural Coworker Agent provides concise cultural insights, "
                "trends, and travel recommendations for any country.\n\n"
                "Primary functions:\n"
                "- Analyze cultural behavior and etiquette\n"
                "- Suggest marketing or engagement strategies\n"
                "- Recommend local activities and food highlights\n\n"
                "Built with FastAPI and powered by Gemini 2.5 Flash. Fully compatible with Telex.im REST API integration."
            ),
            "name": "Telex Cultural Coworker",
            "node": [
                {
                    "id": "cultural_agent",
                    "name": "Cultural Insight Agent",
                    "parameters": {},
                    "position": [520, -210],
                    "type": "a2a/generic-a2a-node",
                    "typeVersion": 1,
                    "url": "https://telex-cultural-coworker-production.up.railway.app/a2a/telex-cultural"
                }
            ],
            "short_description": "An AI agent that delivers cultural insights for global engagement.",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "response": {
                "status": "success",
                "location": location,
                "insights": insights
            }
        }

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
