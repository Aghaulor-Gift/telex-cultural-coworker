from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.gemini_service import get_cultural_insights
from app.models.schemas import InsightResponse
from app.config import logger

router = APIRouter()


@router.get("/insights", response_model=InsightResponse)
async def get_insight(location: str):
    """
    Retrieves structured cultural insights for a given location
    using the Gemini 2.5 Flash API.

    Args:
        location (str): The city or country to get insights for.

    Returns:
        JSONResponse: A structured dictionary containing cultural,
        social, and marketing insights.
    """
    logger.info(f"API Call: Retrieving insights for location: {location}")

    try:
        # Fetch structured AI insights (dict)
        insights = await get_cultural_insights(location)

        # Build final response format
        formatted_result = {
            "status": "success",
            "location": location,
            "insights": insights
        }

        return JSONResponse(content=formatted_result, status_code=200)

    except Exception as e:
        logger.error(f"Error retrieving insights for {location}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error while retrieving insights for {location}"
        )
