from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.gemini_service import get_cultural_insights
from app.models.schemas import InsightResponse

router = APIRouter()

@router.get("/insights", response_model=InsightResponse)
async def get_insight(location: str):
    # ✅ remove 'await' since get_cultural_insights is synchronous
    result = get_cultural_insights(location)
    
    formatted_result = {
        "status": "success",
        "response": {
            "location": location,
            "insights": result.replace("\\n", "\n\n")
        }
    }

    return JSONResponse(content=formatted_result)
