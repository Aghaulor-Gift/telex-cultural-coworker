import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Basic Logger setup
logger = logging.getLogger("telex_cultural_agent")
logger.setLevel(logging.INFO)

# Console handler for Railway logs
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

# Agent Metadata
AGENT_ID = os.getenv("AGENT_ID", "telex-cultural-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Telex Cultural Coworker")
AGENT_DESCRIPTION = os.getenv("AGENT_DESCRIPTION", "AI-powered cultural coworker that gives location-based insights.")
AGENT_DOMAIN = os.getenv("AGENT_DOMAIN", "https://telex-cultural-coworker-production.up.railway.app")

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
