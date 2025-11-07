from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from app.services.gemini_service import get_cultural_insights
from app.config import logger, AGENT_ID, AGENT_NAME, AGENT_DESCRIPTION, AGENT_DOMAIN
from datetime import datetime

router = APIRouter()
A2A_PATH = "/a2a/telex-cultural"


@router.get("/.well-known/agent.json", include_in_schema=False)
def get_agent_card():
    """Returns metadata describing the Telex Cultural Coworker Agent."""
    webhook_url = f"{AGENT_DOMAIN}/api/v1{A2A_PATH}"

    agent_card = {
        "active": True,
        "category": "Cultural Insights and Marketing",
        "description": AGENT_DESCRIPTION,
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
        "short_description": "AI cultural coworker providing global marketing and etiquette insights.",
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


@router.post(A2A_PATH, include_in_schema=False)
async def telex_webhook(request: Request):
    """
    Handles Telex webhook requests — supports A2A JSON-RPC, params, and simplified payloads.
    """
    try:
        body = await request.json()
        logger.info(f"Incoming payload: {body}")

        # Detect A2A format
        is_a2a_format = "jsonrpc" in body or "method" in body

        # Extract location flexibly
        location = (
            body.get("location") or
            body.get("data", {}).get("location") or
            body.get("params", {}).get("location") or
            None
        )

        if not location:
            logger.warning("Missing 'location' parameter in request.")
            return JSONResponse(
                content={"error": "Missing 'location' parameter in request body."},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"Received request for location: {location}")

        # Get insights
        try:
            insights = await get_cultural_insights(location)
        except Exception as e:
            logger.warning(f"Gemini service failed, using fallback. Error: {e}")
            insights = {
                "culture": f"{location} has a diverse and deeply rooted cultural identity.",
                "communication_style": f"People in {location} often communicate politely and respectfully.",
                "business_etiquette": f"In {location}, punctuality and courtesy are highly valued.",
                "food_and_cuisine": f"{location} offers a mix of traditional and modern cuisines.",
                "lifestyle_and_customs": f"The lifestyle in {location} reflects community, family, and tradition.",
                "dress_code": f"Attire in {location} varies by occasion, reflecting respect and modesty.",
                "marketing_tips": f"Effective marketing in {location} focuses on authenticity and community ties.",
                "travel_recommendations": f"Explore landmarks, nature, and festivals to experience {location}.",
                "festivals_and_celebrations": f"{location} celebrates many vibrant festivals throughout the year."
            }

        # Build response
        response_payload = {
            "active": True,
            "category": "Cultural Insights and Marketing",
            "description": AGENT_DESCRIPTION,
            "id": AGENT_ID,
            "name": AGENT_NAME,
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
