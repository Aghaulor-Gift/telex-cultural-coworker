from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from app.services.gemini_service import get_cultural_insights
from app.config import logger, AGENT_ID, AGENT_NAME, AGENT_DESCRIPTION, AGENT_DOMAIN
from datetime import datetime

router = APIRouter()
A2A_PATH = "/a2a/telex-cultural"


# --- 1️⃣ AGENT CARD ENDPOINT ---
@router.get("/.well-known/agent.json", include_in_schema=False)
def get_agent_card():
    """Returns metadata describing the Telex Cultural Coworker Agent."""
    webhook_url = f"{AGENT_DOMAIN}/api/v1{A2A_PATH}"

    agent_card = {
        "active": True,
        "category": "Cultural Insights and Marketing",
        "description": "An AI agent that provides real-time cultural insights for global engagement and marketing.",
        "id": AGENT_ID,
        "name": AGENT_NAME,
        "long_description": (
            "The Telex Cultural Coworker Agent delivers AI-powered insights about cultures worldwide — "
            "including etiquette, cuisine, lifestyle, and business norms. It helps organizations, creators, "
            "and travelers understand global diversity.\n\n"
            "Features:\n"
            "- Analyze cultural behavior and etiquette\n"
            "- Suggest marketing and engagement strategies\n"
            "- Recommend food, festivals, and travel highlights\n\n"
            "Built with FastAPI and Gemini 2.5 Flash, designed for seamless Telex.im A2A integration."
        ),
        "short_description": "AI cultural insight and marketing coworker",
        "nodes": [
            {
                "id": "cultural_agent",
                "name": "Cultural Insight Agent",
                "parameters": {},
                "position": [700, -120],
                "type": "a2a/generic-a2a-node",
                "typeVersion": 1,
                "url": webhook_url
            }
        ],
        "pinData": {},
        "settings": {"executionOrder": "v1"},
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    logger.info("Serving Telex Agent Definition (Agent Card).")
    return JSONResponse(content=agent_card)


# --- 2️⃣ MAIN WEBHOOK ENDPOINT ---
@router.post(A2A_PATH, include_in_schema=False)
async def telex_webhook(request: Request):
    """
    Handles Telex webhook requests — supports both A2A JSON-RPC and simplified data payloads.
    """
    try:
        body = await request.json()

        # Allow both A2A-compliant and simplified payloads
        jsonrpc = body.get("jsonrpc", "2.0")
        req_id = body.get("id", "auto-id")
        method = body.get("method", "cultural_insights")
        data = body.get("data", {})
        location = data.get("location")

        if not location:
            logger.warning("Missing 'location' parameter in request.")
            return JSONResponse(
                content={"error": "Missing 'location' parameter."},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"Processing A2A request for location: {location}")

        # --- Fetch Insights from Gemini ---
        try:
            insights = await get_cultural_insights(location)
        except Exception as e:
            logger.warning(f"Gemini service failed, returning fallback insights: {e}")
            insights = {
                "culture": f"{location} is known for its diverse cultural heritage and values.",
                "communication_style": f"People in {location} often communicate with politeness and respect.",
                "business_etiquette": f"In {location}, punctuality and formality are valued in business meetings.",
                "food_and_cuisine": f"{location} offers a wide range of traditional and modern cuisine.",
                "lifestyle_and_customs": f"Residents of {location} enjoy a vibrant social and family-oriented lifestyle.",
                "dress_code": f"People in {location} dress appropriately for the occasion, respecting local customs.",
                "marketing_tips": f"When marketing in {location}, emphasize trust, authenticity, and community connection.",
                "travel_recommendations": f"Explore famous landmarks, local markets, and cultural festivals in {location}.",
                "festivals_and_celebrations": f"{location} celebrates colorful festivals that highlight its cultural identity."
            }

        # --- Construct the final response ---
        response_payload = {
            "active": True,
            "category": "Cultural Insights and Marketing",
            "description": "An AI agent that provides real-time cultural insights for global engagement and marketing.",
            "id": AGENT_ID,
            "name": AGENT_NAME,
            "long_description": (
                "An AI-powered agent that provides cultural insights, etiquette, lifestyle tips, "
                "and marketing recommendations for any country or region."
            ),
            "short_description": "AI cultural coworker providing insights across countries.",
            "nodes": [
                {
                    "id": "cultural_agent",
                    "name": "Cultural Insight Agent",
                    "parameters": {},
                    "position": [700, -120],
                    "type": "a2a/generic-a2a-node",
                    "typeVersion": 1,
                    "url": f"{AGENT_DOMAIN}/api/v1{A2A_PATH}"
                }
            ],
            "pinData": {},
            "settings": {"executionOrder": "v1"},
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
