from pydantic import BaseModel, Field
from typing import Optional, Literal

# --- A2A Request Models ---
class A2AData(BaseModel):
    location: str = Field(..., description="The city or country to get insights for (e.g., 'Tokyo', 'Brazil').")

class A2ARequest(BaseModel):
    jsonrpc: Literal["2.0"]
    id: str = Field(..., description="Unique request identifier")
    method: str = Field(..., description="The name of the method to invoke, e.g. 'cultural_insights'.")
    data: Optional[A2AData] = Field(None, description="Input parameters for the method.")


# --- Insight Response Schema ---
class InsightDetail(BaseModel):
    culture: str
    communication_style: str
    business_etiquette: str
    food_and_cuisine: str
    lifestyle_and_customs: str
    dress_code: str
    marketing_tips: str
    travel_recommendations: str
    festivals_and_celebrations: str

class InsightResponse(BaseModel):
    status: str
    location: str
    insights: InsightDetail
