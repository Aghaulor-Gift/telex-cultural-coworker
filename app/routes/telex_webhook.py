from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.models.schemas import A2ARequest
from app.services.gemini_service import get_cultural_insights
from app.config import logger, AGENT_ID, AGENT_NAME, AGENT_DESCRIPTION, AGENT_DOMAIN
from datetime import datetime

router = APIRouter()
A2A_PATH = "/a2a/telex-cultural"

# --- 1️⃣ AGENT CARD ENDPOINT ---
@router.get("/.well-known/agent.json", include_in_schema=False)
def get_agent_card():
    """
    Returns metadata describing the Telex Cultural Coworker Agent.
    """
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
        "settings": {
            "executionOrder": "v1"
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    logger.info("Serving Telex Agent Definition (Agent Card).")
    return JSONResponse(content=agent_card)


# --- 2️⃣ MAIN WEBHOOK ENDPOINT ---
@router.post(A2A_PATH, include_in_schema=False)
async def telex_webhook(request: A2ARequest):
    """
    Handles A2A JSON-RPC invoke requests and returns structured cultural insights.
    """
    try:
        # Validate method
        if request.method != "cultural_insights":
            return JSONResponse(
                content={"error": "Unsupported method. Must be 'cultural_insights'."},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        location = getattr(request.data, "location", None)
        if not location:
            return JSONResponse(
                content={"error": "Missing 'location' parameter."},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"Processing A2A request for location: {location}")

        # --- Get AI insights from Gemini ---
        insights = await get_cultural_insights(location)

        # --- Response payload (formatted like your example) ---
        response_payload = {
            "active": True,
            "category": "Cultural Insights and Marketing",
            "description": "An AI agent that provides real-time cultural insights for global engagement and marketing.",
            "id": AGENT_ID,
            "name": "Telex Cultural Coworker",
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
