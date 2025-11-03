from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, Literal 

# --- A2A Request Models ---

class A2AData(BaseModel):
    """
    Data payload for the incoming A2A JSON-RPC 'invoke' request.
    It expects a 'location' parameter.
    """
    location: str = Field(..., description="The city or country to get insights for (e.g., 'Tokyo', 'Brazil').")

class A2ARequest(BaseModel):
    """
    The main JSON-RPC request structure from Telex.
    
    NOTE: 'jsonrpc' uses Literal for the constant value "2.0" (Pydantic v2 compliant).
    """
    jsonrpc: Literal["2.0"]
    id: str = Field(..., description="A unique request identifier.")
    method: str = Field(..., description="The name of the method to invoke (e.g., 'cultural_insights').")
    data: Optional[A2AData] = Field(None, description="Input parameters for the method.")


# --- Insight Response Schema (Used by /api/v1/insights endpoint) ---

class InsightDetail(BaseModel):
    """
    The structured dictionary returned by the Gemini service.
    """
    culture: str = Field(..., description="A summary of core cultural identity and values.")
    communication_style: str = Field(..., description="Tips on local communication style.")
    business_etiquette: str = Field(..., description="Details on punctuality, dress code for business, and formal greetings.")
    food_and_cuisine: str = Field(..., description="Information on local cuisine, signature dishes, and dining customs.")
    lifestyle_and_customs: str = Field(..., description="Balance of work, family, social life, and typical daily routines.")
    dress_code: str = Field(..., description="Guidance on appropriate clothing for social and religious settings.")
    marketing_tips: str = Field(..., description="Key strategies for effective marketing.")
    travel_recommendations: str = Field(..., description="Popular landmarks and travel advice.")
    festivals_and_celebrations: str = Field(..., description="Major local festivals and their significance.")

class InsightResponse(BaseModel):
    """
    Full response schema for the public /api/v1/insights endpoint.
    This uses the structured dictionary payload.
    """
    status: str = Field(..., description="Status of the request (e.g., 'success').")
    location: str = Field(..., description="The geographic location requested.")
    insights: InsightDetail = Field(..., description="The structured cultural insights.")

# NOTE: The full A2A JSON-RPC response models are omitted because the telex_webhook.py
# is configured to return a custom, agent-metadata rich payload instead of the standard JSON-RPC response.
