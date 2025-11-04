# Building the “Telex Cultural Coworker”: My Journey into A2A Agent Integration with Telex.im

## Introduction

As part of the HNG Internship Stage 3, we were tasked with building an AI Agent that connects to Telex.im using the Agent-to-Agent (A2A) communication protocol.

I chose to create Telex Cultural Coworker, an AI-powered FastAPI agent that provides real-time cultural insights about different countries — including etiquette, food, lifestyle, marketing behavior, and travel advice — using the Google Gemini API.

The goal was to build a smart, production-ready agent that:

- Integrates seamlessly with Telex.im via A2A

- Handles JSON-RPC requests correctly

- Returns structured, AI-generated responses

- Demonstrates creativity, clean code, and strong integration quality

## ⚙️ Tech Stack

I used a modern, developer-friendly stack that balances performance and simplicity:

Tool	Purpose
FastAPI	Framework for building async APIs
Google Gemini API	Generates the cultural insights
Pydantic	Handles JSON schema validation
Railway	For deployment and public hosting
Python-dotenv	Manages environment variables
Logging	For request and error monitoring  


## The Concept: A Cultural Intelligence Agent

The idea was simple yet globally relevant — an AI that acts as a cultural coworker for global teams, marketers, or travelers.

When queried with a location (like “Japan” or “Nigeria”), it fetches:

- Core cultural values

- Business etiquette

- Communication styles

- Cuisine highlights

- Lifestyle and traditions

- Marketing insights

- Travel recommendations

It’s like having a digital cultural advisor available through Telex chat.

## Understanding the A2A Protocol

The A2A (Agent-to-Agent) protocol defines how agents communicate within Telex.im.
It expects:

- A public agent card at /.well-known/agent.json

- A POST endpoint that accepts JSON-RPC style requests 
```
(e.g., {"jsonrpc": "2.0", "id": "...", "method": "cultural_insights", "data": {...}})
```

- A structured response containing insights or actions.

Here’s an example of a valid A2A request:
```

{
  "jsonrpc": "2.0",
  "id": "test-001",
  "method": "cultural_insights",
  "data": { "location": "Japan" }
}

```
And the expected response looks like this:
```
{
  "active": true,
  "category": "Cultural Insights and Marketing",
  "id": "telex-cultural-agent",
  "name": "Telex Cultural Coworker",
  "response": {
    "status": "success",
    "location": "Japan",
    "insights": {
      "culture": "Japanese culture emphasizes respect, hierarchy, and harmony...",
      "food_and_cuisine": "Popular dishes include sushi, ramen, and tempura..."
    }
  }
}

```
This means that every request from Telex.im can automatically understand and render the response.

##  Building the Agent
### 1️⃣ Setting Up FastAPI

I created the core FastAPI structure with a simple main.py:
```
from fastapi import FastAPI
from app.routes import telex_webhook, cultural_agent

app = FastAPI(title="Telex Cultural Coworker API")

app.include_router(telex_webhook.router, prefix="/api/v1")
app.include_router(cultural_agent.router, prefix="/api/v1")
```

### 2️⃣ Defining Models with Pydantic

I used schemas.py to define strict models for A2A requests and API responses:
```
class A2ARequest(BaseModel):
    jsonrpc: Literal["2.0"]
    id: str
    method: str
    data: Optional[A2AData]
```

This made it easy to validate Telex requests and ensure proper error handling.

### 3️⃣ The Gemini Integration

Using Google’s Gemini 2.5 Flash API, I built a reusable service that generates JSON-formatted cultural insights:
```
async def get_cultural_insights(location: str) -> dict:
    payload = {
        "contents": [{"parts": [{"text": f"Generate cultural insights for {location}"}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, params={"key": GEMINI_API_KEY}, json=payload)
        return json.loads(response.json()["candidates"][0]["content"]["parts"][0]["text"])
```

## Connecting to Telex (A2A Endpoint)

The Telex webhook (telex_webhook.py) handles requests sent by the platform:
```
@router.post("/a2a/telex-cultural")
async def telex_webhook(request: A2ARequest):
    location = request.data.location
    insights = await get_cultural_insights(location)
    return {
        "active": True,
        "category": "Cultural Insights and Marketing",
        "id": AGENT_ID,
        "name": "Telex Cultural Coworker",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "response": {
            "status": "success",
            "location": location,
            "insights": insights
        }
    }

```
And the /.well-known/agent.json file defines the agent card so Telex can discover and connect to it:
```
{
  "id": "telex-cultural-agent",
  "name": "Telex Cultural Coworker",
  "description": "AI agent that provides global cultural insights",
  "methods": [
    {
      "name": "cultural_insights",
      "parameters": { "location": { "type": "string" } },
      "url": "https://telex-cultural-coworker-production.up.railway.app/api/v1/a2a/telex-cultural"
    }
  ]
}
```

## Deployment on Railway

I chose Railway.app because it provides:

- Fast FastAPI deployments

- Easy environment variable management

- Auto-generated HTTPS domains

## My environment variables:
```
GEMINI_API_KEY=your_gemini_api_key
AGENT_ID=telex-cultural-agent
AGENT_DOMAIN=https://telex-cultural-coworker-production.up.railway.app
```

After setting these, I ran:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then Railway handled the rest — the app went live at
👉 https://telex-cultural-coworker-production.up.railway.app/api/v1/a2a/telex-cultural

## ✅ What Worked

-- A2A JSON Schema Validation worked flawlessly using Pydantic.

-- Gemini Integration returned structured, natural insights.

-- Telex agent discovery via .well-known/agent.json loaded successfully.

-- Logging and error handling made debugging easy.

## ⚠️ What Didn’t (and How I Fixed It)
|Issue|Cause	|Fix|
|-------------------|
|"API key missing" |in production	Railway doesn’t auto-load .env	|Added GEMINI_API_KEY via Railway Variables|  
|JSONResponse indent error|	FastAPI deprecated indent argument|	Removed it
500 errors from Gemini|  
|Missing async handling	Switched to await for async HTTP calls|
|Request validation errors	|Missing JSON-RPC fields	|Added proper A2ARequest Pydantic model|

## Lessons Learned

- A2A is strict — every JSON key matters.

- Telex requires consistent schemas for discoverability.

- Logging is your best friend during integration.

- Environment variables must be set in your hosting platform — not just .env.

- LLM APIs need retry logic (Gemini can time out under heavy load).

## Final Thoughts

Building the Telex Cultural Coworker was a great deep dive into AI + integrations.
It taught me how structured agent communication (A2A) enables interoperability between intelligent systems.

### The final agent now:

Fetches and structures cultural insights via Gemini

Responds to Telex.im queries in real-time

Returns valid A2A JSON payloads

Is live on Railway for global access 🚀

### 👉 Live Agent:
https://telex-cultural-coworker-production.up.railway.app/api/v1/a2a/telex-cultural

### 👉 GitHub Repo:
https://github.com/Aghaulor-Gift/telex-cultural-coworker


#### Example Response
```
{
  "active": true,
  "category": "Cultural Insights and Marketing",
  "name": "Telex Cultural Coworker",
  "id": "telex-cultural-agent",
  "timestamp": "2025-11-03T19:43:04Z",
  "response": {
    "status": "success",
    "location": "Japan",
    "insights": {
      "culture": "Japanese culture emphasizes respect, harmony, and community balance.",
      "business_etiquette": "Always exchange business cards with both hands.",
      "food_and_cuisine": "Popular dishes include sushi, ramen, and regional cuisine."
    }
  }
}
```

## 🧑‍💻 Connect with Me

Author: Aghaulor Gift
GitHub: [Github link](https://github.com/Aghaulor-Gift/telex-cultural-coworker)

Telex Agent: Telex Cultural Coworker

Tags: #HNGInternship #TelexIm #AI #FastAPI #GeminiAPI


