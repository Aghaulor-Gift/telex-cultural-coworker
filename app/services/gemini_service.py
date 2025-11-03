import httpx, json, asyncio
from app.config import logger, GEMINI_API_KEY

GEMINI_MODEL = "gemini-2.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

async def get_cultural_insights(location: str) -> dict:
    """Fetches structured cultural insights from the Gemini API."""
    
    if not GEMINI_API_KEY:
        logger.warning("Gemini API key missing. Returning fallback content.")
        return {
            "culture": f"Culture insights for {location} are unavailable (API key missing).",
            "communication_style": f"Communication style tips for {location} are unavailable (API key missing).",
            "business_etiquette": f"Business etiquette tips for {location} are unavailable (API key missing).",
            "food_and_cuisine": f"Food and cuisine tips for {location} are unavailable (API key missing).",
            "lifestyle_and_customs": f"Lifestyle and customs for {location} are unavailable (API key missing).",
            "dress_code": f"Dress codes for {location} are unavailable (API key missing).",
            "marketing_tips": f"Marketing tips for {location} are unavailable (API key missing).",
            "travel_recommendations": f"Travel recommendations for {location} are unavailable (API key missing).",
            "festivals_and_celebrations": f"Festivals and celebrations for {location} are unavailable (API key missing)."
        }

    system_prompt = (
        "You are a world-class cultural expert. Generate factual, respectful insights about the given location, "
        "including culture, etiquette, cuisine, travel, and marketing recommendations. Output must be JSON."
    )
    user_prompt = f"Generate detailed cultural insights for {location}."

    payload = {
        "contents": [{"parts": [{"text": user_prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {"responseMimeType": "application/json"},
    }

    headers = {"Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(f"{API_URL}?key={GEMINI_API_KEY}", headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            json_text = result["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(json_text)
    except Exception as e:
        logger.error(f"Gemini API call failed: {e}")
        return {"error": f"Failed to fetch AI insights for {location}."}
