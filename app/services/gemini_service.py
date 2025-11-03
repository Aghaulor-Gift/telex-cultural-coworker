import httpx
import json
import asyncio 
from app.config import logger, GEMINI_API_KEY

# The model used for generating structured, factual text content
GEMINI_MODEL = "gemini-2.5-flash-preview-09-2025"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

async def get_cultural_insights(location: str) -> dict:
    """
    Retrieves cultural insights for a given location using the Gemini API (REST).
    
    The function enforces a strict JSON schema for the output to ensure
    the resulting dictionary matches the required structure for the agent.
    """
    if not GEMINI_API_KEY:
        logger.error("API Key not found. Cannot call Gemini Service.")
        # Return a mock response structure for safe fallback
        return {
            "culture": f"Culture insights for {location} are unavailable (API key missing).",
            "communication_style": f"Communication style tips for {location} are unavailable (API key missing).",
            "business_etiquette": f"Business etiquette tips for {location} are unavailable (API key missing).",
            "food_and_cuisine": f"Food and cuisine tips for {location} are unavailable (API key missing).",
            "lifestyle_and_customs": f"Lifestyle and customs for {location} are unavailable (API key missing).",
            "dress_code": f"Dress codes for {location} are unavailable (API key missing).",
            "marketing_tips": f"Marketing tips for {location} are unavailable (API key missing).",
            "travel_recommendations": f"Travel recommendations for {location} are unavailable (API key missing).",
            "festivals_and_celebrations": f"Festivals and celebrations for {location} are unavailable (API key missing).",
        }

    # 1. System Instruction and User Query
    system_prompt = (
        "You are a world-class cultural expert and marketer. Generate detailed, accurate cultural insights "
        "for the provided location. The response MUST be a JSON object that strictly adheres to the "
        "provided schema. Each generated string must be professional, factual, and informative. "
        "Focus on practical tips for travelers and businesses."
    )

    user_query = f"Provide comprehensive cultural insights, etiquette, cuisine details, and marketing tips for: {location}"

    # 2. JSON Schema defining the required output structure
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "culture": {"type": "STRING", "description": "Summary of core cultural identity and values (e.g., respect, hierarchy)."},
            "communication_style": {"type": "STRING", "description": "Tips on local communication, politeness, and handling disagreements."},
            "business_etiquette": {"type": "STRING", "description": "Details on punctuality, dress code for business, and formal greetings."},
            "food_and_cuisine": {"type": "STRING", "description": "Information on local cuisine, signature dishes, and dining customs."},
            "lifestyle_and_customs": {"type": "STRING", "description": "Balance of work, family, social life, and typical daily routines."},
            "dress_code": {"type": "STRING", "description": "Guidance on appropriate clothing for social and religious settings."},
            "marketing_tips": {"type": "STRING", "description": "Key strategies for effective marketing (e.g., trust, local storytelling)."},
            "travel_recommendations": {"type": "STRING", "description": "Popular landmarks, unique experiences, and local travel advice."},
            "festivals_and_celebrations": {"type": "STRING", "description": "Major local festivals, their significance, and typical activities."}
        },
        "required": [
            "culture", "communication_style", "business_etiquette", "food_and_cuisine", 
            "lifestyle_and_customs", "dress_code", "marketing_tips", "travel_recommendations", 
            "festivals_and_celebrations"
        ]
    }
    
    # 3. Construct the API Payload
    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "tools": [{"google_search": {} }],  # Enable grounding for up-to-date information
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    # 4. Exponential Backoff and Retry Logic
    max_retries = 3
    delay = 1
    logger.info(f"Fetching insights from Gemini for: {location}")
    
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{API_URL}?key={GEMINI_API_KEY}", 
                    headers=headers, 
                    content=json.dumps(payload)
                )
                response.raise_for_status() # Raises exception for 4xx/5xx status codes
                
                result = response.json()
                
                # Extract the JSON string from the response and parse it
                json_text = result['candidates'][0]['content']['parts'][0]['text']
                insights_dict = json.loads(json_text)
                return insights_dict

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error on attempt {attempt + 1}: {e.response.status_code} - {e.response.text}")
            if e.response.status_code in [429, 500, 503] and attempt < max_retries - 1:
                logger.info(f"Retrying in {delay}s...")
                await asyncio.sleep(delay)
                delay *= 2
            else:
                raise Exception(f"Failed to get insights after {max_retries} attempts: {e}")
                
        except Exception as e:
            logger.error(f"An unexpected error occurred during API call: {e}")
            raise e
            
    # Should be unreachable
    raise Exception("API call failed after all retries.")
