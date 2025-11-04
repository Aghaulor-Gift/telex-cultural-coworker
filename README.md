#  Telex Cultural Coworker

**Telex Cultural Coworker** is an intelligent FastAPI-based service that provides cultural and social insights about different countries and locations using the **Google Gemini API**.  
The API integrates with Redis for caching responses and delivers well-structured JSON outputs for easy integration into other systems or applications.

---

##  Features

- Fetches **cultural insights** about any location (e.g., Japan, Nigeria, France)
- Built with **FastAPI** for high performance and scalability
- Uses **Gemini AI** for generating intelligent, context-aware responses
- Integrates **Redis caching** for faster repeated queries
- Structured API response in **JSON format**
- Modular, clean, and production-ready architecture

---

## 🧩 Project Structure
app/
├── __init__.py  
├── config.py                # App configuration and environment variables  
├── main.py                  # FastAPI app entry point  
│  
├── models/  
│   ├── __init__.py  
│   └── schemas.py           # Pydantic request/response models  
│  
├── routes/  
│   ├── __init__.py  
│   ├── cultural_agent.py    # /api/v1/insights endpoint  
│   └── telex_webhook.py     # /api/v1/a2a/telex-cultural (Telex integration)  
│
├── services/  
│   ├── __init__.py  
│   ├── gemini_service.py    # Gemini API communication logic  
│   └── cache_service.py     # (Optional) Redis caching module  
│
└── telex_venv/              # Local virtual environment (ignored in git)  


## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/telex-cultural-coworker.git
cd telex-cultural-coworker
```

## Create and Activate a Virtual Environment
python3 -m venv telex_venv
source telex_venv/bin/activate   # On Windows: telex_venv\Scripts\activate


## Install Dependencies
```
pip install -r requirements.txt
```

## Configure Environment Variables
```
GEMINI_API_KEY=your_gemini_api_key_here
AGENT_DOMAIN=https://telex-cultural-coworker-production.up.railway.app
AGENT_ID=telex-cultural-agent
AGENT_NAME=Telex Cultural Coworker
AGENT_DESCRIPTION=AI agent providing cultural insights globally
REDIS_URL=redis://localhost:6379
```

## Start Redis (if not already running)
```
sudo service redis-server start
```

## Run the Application
```
./run.sh start
```
Or manually with Uvicorn:
```
uvicorn app.main:app --reload
```


---
## Core Functionalities
| Feature                | Description                                                    |
| ---------------------- | -------------------------------------------------------------- |
| **Cultural Insights**  | Retrieves AI-generated cultural summaries and etiquette tips   |
| **Gemini Integration** | Uses Google’s Gemini model for contextual and accurate outputs |
| **Telex A2A Protocol** | Provides structured JSON responses compatible with Telex.im    |
| **FastAPI Framework**  | Handles routing and high-performance API responses             |
| **Logging**            | Provides detailed logs for monitoring and debugging            |


## 🧩 Key API Endpoints

| Endpoint                          | Method | Description                                              |
| --------------------------------- | ------ | -------------------------------------------------------- |
| `/api/v1/health`                  | GET    | Health check endpoint                                    |
| `/api/v1/insights?location=Japan` | GET    | Fetch insights for a given location                      |
| `/api/v1/a2a/telex-cultural`      | POST   | A2A endpoint used by Telex.im to fetch cultural insights |
| `/.well-known/agent.json`         | GET    | Agent card definition for Telex discovery                |


## 🧰 Tech Stack

| Category                   | Tools             |
| -------------------------- | ----------------- |
| **Framework**              | FastAPI           |
| **AI Engine**              | Google Gemini API |
| **Language**               | Python 3.12       |
| **Environment Management** | python-dotenv     |
| **Logging**                | Python Logging    |
| **Deployment**             | Railway (Uvicorn) |


---

## 🧾 Environment Variables (.env)
| Variable            | Description                                    |
| ------------------- | ---------------------------------------------- |
| `GEMINI_API_KEY`    | Your Gemini API key from Google AI Studio      |
| `AGENT_DOMAIN`      | Public domain of your deployed agent           |
| `AGENT_ID`          | Unique identifier for your Telex agent         |
| `AGENT_NAME`        | Display name of your AI agent                  |
| `AGENT_DESCRIPTION` | Description of your agent for Telex registry   |
| `REDIS_URL`         | Redis connection string (optional for caching) |


## Troubleshooting

| Issue                             | Cause                        | Fix                                       |
| --------------------------------- | ---------------------------- | ----------------------------------------- |
| **"API key missing" in insights** | Railway not loading `.env`   | Add `GEMINI_API_KEY` in Railway Variables |
| **500 Internal Server Error**     | Gemini API unavailable       | Check logs in Railway and verify API key  |
| **Redis connection error**        | Redis not running            | Start Redis or disable caching in code    |
| **Indent error in JSONResponse**  | `indent` argument deprecated | Removed in final version ✅                |



## Requirements.txt (for reference)
```
fastapi
uvicorn
redis
python-dotenv
google-generativeai
pydantic
```


## API Usage
### Endpoint: /api/v1/insights

#### Method: GET

#### Query Parameter:

- location (string): The name of the country or region you want insights for.
#### Example Requests
#### Get Cultural Insights (Direct)
```
GET https://telex-cultural-coworker-production.up.railway.app/api/v1/insights?location=Kenya
```
#### Example Response:
```
{
  "status": "success",
  "response": {
    "location": "Kenya",
    "insights": {
      "culture": "Kenyan culture emphasizes community, hospitality, and respect for elders.",
      "food_and_cuisine": "Staple foods include ugali, sukuma wiki, and nyama choma.",
      "business_etiquette": "Punctuality and professional dress are important in meetings."
    }
  }
}
```

#### Telex A2A Integration (POST)
```
POST https://telex-cultural-coworker-production.up.railway.app/api/v1/a2a/telex-cultural
```

#### Body:
```
{
  "jsonrpc": "2.0",
  "id": "test-001",
  "method": "cultural_insights",
  "data": {
    "location": "USA"
  }
}
```

#### Response Example:
```
{
  "active": true,
  "category": "Cultural Insights and Marketing",
  "id": "telex-cultural-agent",
  "name": "Telex Cultural Coworker",
  "short_description": "AI cultural coworker providing insights across countries.",
  "timestamp": "2025-11-03T19:43:04.762602Z",
  "response": {
    "status": "success",
    "location": "USA",
    "insights": {
      "culture": "American culture values individuality, freedom, and innovation.",
      "communication_style": "Direct and open communication is appreciated.",
      "business_etiquette": "Be punctual and confident in presentations.",
      "food_and_cuisine": "Diverse regional cuisines such as BBQ, Cajun, and Tex-Mex.",
      "marketing_tips": "Emphasize authenticity and innovation in campaigns."
    }
  }
}
```


🧑‍💻 Author

Developed by: Aghaulor Gift  
Email: [Email](aghaulor.gift@gmail.com)  
GitHub: [Github Link](https://github.com/Aghaulor-Gift/telex-cultural-coworker)  
Deployed on: [Railway](https://telex-cultural-coworker-production.up.railway.app)