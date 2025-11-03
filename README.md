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
├── pycache/ # Compiled Python cache files  
│
├── models/ # Data models (schemas and validation)  
│ ├── init.py  
│ └── schemas.py # Defines request/response Pydantic schemas  
│  
├── routes/ # Application endpoints      
│ ├── init.py  
│ ├── cultural_agent.py # Route for cultural insights endpoint  
│ └── telex_webhook.py # Route for Telex webhook integration  
│  
├── services/ # Business logic and integrations  
│ ├── init.py  
│ ├── cache_service.py # Redis caching and retrieval logic  
│ ├── gemini_service.py # Handles communication with Gemini API  
│ ├── config.py # Environment variable and app config  
│ └── main.py # FastAPI app instance and route mounting  
│  
└── telex_venv/ # Local Python virtual environment  


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

## ⚙️ Core Functionalities

- **FastAPI Framework**: Handles HTTP requests and routing.
- **Gemini API Integration**: Provides AI-generated cultural insights.
- **Redis Cache Layer**: Optimizes performance by caching frequent queries.
- **Telex Webhook**: Enables communication with Telex platform.
- **Environment Configuration**: Managed via `.env` and `config.py`.

---

## 🧩 Key Files and Responsibilities

| File | Description |
|------|--------------|
| `cultural_agent.py` | Endpoint that generates cultural insights for requested locations. |
| `telex_webhook.py` | Endpoint to receive and respond to Telex webhook requests. |
| `gemini_service.py` | Manages requests and responses to/from Google Gemini AI. |
| `cache_service.py` | Stores and retrieves data using Redis caching. |
| `config.py` | Loads environment variables and config settings. |
| `main.py` | Initializes the FastAPI app and includes route registration. |
| `schemas.py` | Defines Pydantic models for request and response validation. |
| `run.sh` | Bash script for starting/stopping the FastAPI server. |

---

## 🧰 Tech Stack

| Category | Tools Used |
|-----------|-------------|
| **Framework** | FastAPI |
| **AI Integration** | Google Gemini API |
| **Cache Database** | Redis |
| **Language** | Python 3.x |
| **Environment Management** | python-dotenv |
| **Deployment** | Uvicorn |
| **Package Management** | pip, npm (optional) |

---

## 🧾 Environment Variables (.env)



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
#### Example Request:
```
GET http://127.0.0.1:8000/api/v1/insights?location=Japan
```
#### Example Response:
```
{
  "location": "Japan",
  "insight": "Japan is a country with a rich cultural heritage, blending ancient traditions with modern innovation..."
}
```

| Component               | Description                            |
| ----------------------- | -------------------------------------- |
| **FastAPI**             | Web framework powering the API         |
| **Gemini API**          | Generates cultural insights            |
| **Redis**               | Stores cached responses for efficiency |
| **Pydantic (Optional)** | Defines structured API response models |
| **Logging**             | Tracks API requests and errors         |


## Development Notes

- The API automatically connects to Redis at startup.

- If Gemini API or Redis connection fails, errors are logged gracefully.

- Responses are returned using FastAPI’s JSONResponse.

- Removed unsupported argument indent from JSONResponse() to ensure compatibility with latest FastAPI versions.

## Troubleshooting
| Issue                                                                            | Possible Fix                                                            |
| -------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `TypeError: JSONResponse.__init__() got an unexpected keyword argument 'indent'` | Remove the `indent` argument from the `JSONResponse()` call.            |
| Redis not connecting                                                             | Ensure Redis server is running and `.env` contains correct `REDIS_URL`. |
| 500 Internal Server Error                                                        | Check logs for Gemini API response issues or network errors.            |


🧑‍💻 Author

Developed by: Aghaulor Gift  
Email: [Email](aghaulor.gift@gmail.com)  
GitHub: [Github Link](https://github.com/Aghaulor-Gift)