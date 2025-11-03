import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Logging setup ---
logger = logging.getLogger("telex_cultural_agent")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

# --- Agent Metadata (For Telex integration) ---
AGENT_ID = os.getenv("AGENT_ID", "telex-cultural-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Telex Cultural Coworker")
AGENT_DESCRIPTION = os.getenv(
    "AGENT_DESCRIPTION",
    "AI-powered cultural coworker that provides global cultural insights and etiquette tips."
)
AGENT_DOMAIN = os.getenv(
    "AGENT_DOMAIN",
    "https://telex-cultural-coworker-production.up.railway.app"
)

# --- Gemini API Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
