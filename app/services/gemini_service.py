import google.generativeai as genai
from app.config import GEMINI_API_KEY, logger

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)

def get_cultural_insights(location: str) -> str:
    """Generate cultural insights, trending topics, and travel advice for a given location."""
    try:
        prompt = f"""
        You are an AI cultural analyst.
        Provide insights about {location} including:
        1. Cultural summary (customs, traditions, and social etiquette)
        2. Food and cuisine highlights
        3. Trending or popular activities
        4. Travel or marketing recommendations

        Respond in concise paragraphs and add a space to the paragraphs for readability.
        Add headings for each section.
        Format the response in markdown.
        Bullet point lists are encouraged where appropriate.
        Ensure the response is engaging and informative.
        
        """

        logger.info(f"Sending prompt to Gemini for: {location}")
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        if response and response.text:
            return response.text.strip()
        else:
            return f"No insights available for {location}."
        

    except Exception as e:
        logger.error(f"Error getting insights for {location}: {e}")
        return f"Could not retrieve insights for {location}."
