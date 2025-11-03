from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.gemini_service import get_cultural_insights
from app.models.schemas import InsightResponse
from app.config import logger

# Initialize the APIRouter
router = APIRouter()

@router.get("/insights", response_model=InsightResponse)
def get_insight(location: str):
    """
    Retrieves cultural insights for a specified location using the Gemini service.
    
    Args:
        location: The geographic location (city, country) to get insights for.
    
    Returns:
        A JSON response containing the location and the generated insights.
    """
    logger.info(f"API Call: Retrieving insights for location: {location}")
    
    # get_cultural_insights is designed to be synchronous, so no 'await' is needed.
    result = get_cultural_insights(location)
    
    # Prepare the response structure. The replace operation helps ensure 
    # markdown formatting from the LLM looks correct in various clients.
    formatted_result = {
        "status": "success",
        "response": {
            "location": location,
            "insights": result.replace("\\n", "\n\n")
        }
    }

    # Return the formatted response, which FastAPI will validate against InsightResponse
    return JSONResponse(content=formatted_result)