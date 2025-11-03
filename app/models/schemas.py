from pydantic import BaseModel

class InsightsDetail(BaseModel):
    location: str
    insights: str

class InsightResponse(BaseModel):
    status: str
    response: InsightsDetail