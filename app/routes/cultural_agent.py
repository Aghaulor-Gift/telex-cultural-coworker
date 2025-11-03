from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.gemini_service import get_cultural_insights
from app.config import logger

router = APIRouter()

@router.get("/insights")
async def get_insight(location: str):
    """Retrieve cultural insights for a location."""
    logger.info(f"Fetching insights for {location}")
    try:
        result = await get_cultural_insights(location)
        return JSONResponse(content={
            "status": "success",
            "location": location,
            "insights": result
        })
    except Exception as e:
        logger.error(f"Error retrieving insights for {location}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
