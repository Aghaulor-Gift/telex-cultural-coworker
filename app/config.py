import os
import logging
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

# --- Logger setup ---
logger = logging.getLogger("telex_cultural_agent")
logger.setLevel(logging.INFO)

# Avoid adding duplicate handlers (important for Uvicorn reload)
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(console_handler)

# --- Agent Metadata (Telex A2A) ---
AGENT_ID = os.getenv("AGENT_ID", "telex-cultural-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Telex Cultural Coworker")
AGENT_DESCRIPTION = os.getenv(
    "AGENT_DESCRIPTION",
    "AI-powered cultural coworker that provides country-based insights, etiquette, and market intelligence."
)
AGENT_DOMAIN = os.getenv(
    "AGENT_DOMAIN",
    "https://telex-cultural-coworker-production.up.railway.app"  # update with your actual domain if needed
)

# --- Gemini API Key (LLM integration) ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Quick warning if key is missing
if not GEMINI_API_KEY:
    logger.warning(" GEMINI_API_KEY not found in environment. Insights will use fallback responses.")
