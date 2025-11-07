from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from app.services.gemini_service import get_cultural_insights
from app.config import logger, AGENT_ID, AGENT_NAME, AGENT_DESCRIPTION, AGENT_DOMAIN
from datetime import datetime
import re
import httpx

router = APIRouter()
A2A_PATH = "/a2a/telex-cultural"


@router.get("/.well-known/agent.json", include_in_schema=False)
def get_agent_card():
    """Serve the Telex Cultural Coworker Agent metadata."""
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
                "url": webhook_url,
            }
        ],
        "pinData": {},
        "settings": {"executionOrder": "v1"},
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    logger.info("Serving Telex Agent Definition (Agent Card).")
    return JSONResponse(content=agent_card)


@router.post(A2A_PATH, include_in_schema=False)
async def telex_webhook(request: Request):
    """Handle Telex webhook requests — supports JSON-RPC, data, or message formats."""
    try:
        body = await request.json()
        logger.info(f"Incoming payload: {body}")

        # --- Step 1: Extract the location ---
        location = (
            body.get("location")
            or body.get("data", {}).get("location")
            or body.get("params", {}).get("location")
        )

        # If Telex sends message/send type payload
        if not location and "params" in body:
            parts = (
                body.get("params", {})
                .get("message", {})
                .get("parts", [])
            )
            for part in parts:
                if part.get("kind") == "text":
                    match = re.search(
                        r"\b(?:about|from|in|of)\s+([A-Z][a-zA-Z]+)\b",
                        part.get("text", "")
                    )
                    if match:
                        location = match.group(1)
                        break

        if not location:
            logger.warning("Missing 'location' parameter in request.")
            return JSONResponse(
                content={"error": "Missing 'location' parameter in request body."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        logger.info(f"Extracted location: {location}")

        # --- Step 2: Fetch cultural insights ---
        try:
            insights = await get_cultural_insights(location)
        except Exception as e:
            logger.warning(f"Gemini service failed, using fallback insights: {e}")
            insights = {
                "culture": f"{location} is known for its diverse traditions and rich social heritage.",
                "communication_style": f"People in {location} value polite, respectful, and contextual communication.",
                "business_etiquette": f"In {location}, punctuality and formality are respected in business culture.",
                "food_and_cuisine": f"{location}'s cuisine reflects cultural diversity and regional flavor.",
                "lifestyle_and_customs": f"Daily life in {location} emphasizes family, community, and celebration.",
                "dress_code": f"Attire in {location} tends to be modest and occasion-appropriate.",
                "marketing_tips": f"Marketing in {location} should emphasize trust, community, and authenticity.",
                "travel_recommendations": f"Explore {location}'s cultural landmarks, markets, and festivals.",
                "festivals_and_celebrations": f"{location} hosts lively festivals showcasing art, food, and music."
            }

        # --- Step 3: Build agent response payload ---
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
                "insights": insights,
            },
        }

        # --- Step 4: If Telex expects push notification, send it back to UI ---
        push_config = (
            body.get("params", {})
                .get("configuration", {})
                .get("pushNotificationConfig", {})
        )
        push_url = push_config.get("url")
        push_token = push_config.get("token")

        if push_url and push_token:
    logger.info(f"Pushing insights back to Telex for {location}...")
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                push_url,
                headers={"Authorization": f"Bearer {push_token}"},
                json={
                    "kind": "message",
                    "role": "assistant",
                    "parts": [
                        {
                            "kind": "text",
                            "text": (
                                f"🌍 **Cultural Insights for {location}:**\n\n"
                                f"**Culture:** {insights.get('culture', 'N/A')}\n\n"
                                f"**Communication Style:** {insights.get('communication_style', 'N/A')}\n\n"
                                f"**Business Etiquette:** {insights.get('business_etiquette', 'N/A')}\n\n"
                                f"**Food & Cuisine:** {insights.get('food_and_cuisine', 'N/A')}\n\n"
                                f"**Lifestyle & Customs:** {insights.get('lifestyle_and_customs', 'N/A')}\n\n"
                                f"**Festivals & Celebrations:** {insights.get('festivals_and_celebrations', 'N/A')}\n\n"
                                f"✨ *Powered by Telex Cultural Coworker*"
                            ),
                        }
                    ],
                },
            )
        logger.info(f"Successfully pushed insights for {location} to Telex UI.")
    except Exception as push_err:
        logger.error(f"Failed to push response to Telex: {push_err}")


        # --- Step 5: Return success response to Telex backend ---
        return JSONResponse(content=response_payload, status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"A2A Webhook Internal Error: {e}")
        return JSONResponse(
            content={"error": "Internal Server Error during insight generation."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
