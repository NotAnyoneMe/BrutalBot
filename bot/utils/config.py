import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env
load_dotenv()

# ---------------------------- 
# Logging setup
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ----------------------------
# Bot credentials
# ----------------------------
TOKEN = os.getenv("TOKEN")
BOT_NAME = os.getenv("BOT_NAME", "BrutalBot")
BOT_USERNAME = os.getenv("BOT_USERNAME", "@BrutalBot")
MONGODB_URI = os.getenv("MONGO_URI")
ADMINS_IDS = []  # add admin Telegram IDs if needed

if not TOKEN:
    raise ValueError("TOKEN not found in .env file")

if not MONGODB_URI:
    raise ValueError("MONGO_URI not found in .env file")

MONGO = MongoClient(MONGODB_URI)
COLLECTION = MONGO["BrutalBot"]

BOT_DESCRIPTION = f"Hello I'm {BOT_NAME} The bot that tells you the truth without mercy 😈"
DEFAULT_LANGUAGE = "EN"
MAX_RESPONSE_LENGTH = 4096  # max chars for AI response

# ----------------------------
# Payment / Debug / Features
# ----------------------------
PAYMENT_CUR = "XTR"
DEBUG = True
ENABLE_REFERRALS = True
LOG_FILE = os.getenv("LOG_FILE", "bot.log")

# ----------------------------
# Response modes
# ----------------------------
RESPONSE_MODES = {
    "brutal": "😈",
    "philosophical": "🧠",
    "sarcastic": "😂"
}

# ----------------------------
# Sharing / Social
# ----------------------------
SHARE_BUTTON = "Share Brutal"
SHARE_AS_IMAGE = True
SHARE_PLATFORM = ["tiktok", "telegram", "x.com"]
SHARE_MESSAGE = "Ready to hear the truth that no one can bear? 👀"

# ----------------------------
# User interaction
# ----------------------------
ALLOW_USER_MODE_SELECTION = True
STORE_CONVERSATION = False
BLOCK_OFFENSIVE_WORDS = True

# ----------------------------
# AI configuration
# ----------------------------
USE_AI = True
GEMINI_KEY = os.getenv("GEMINI_KEY")

if not GEMINI_KEY:
    raise ValueError("GEMINI_KEY not found in .env file")

# AI prompt template
AI_PROMPT_TEMPLATE = """You are a Telegram bot named BrutalBot. Your main mission is to respond to user messages with brutal honesty. You do not soften the truth or sugarcoat anything. You reveal hidden flaws, weaknesses, or uncomfortable truths about the user in a shocking and impactful way.

Important instructions:
1. Keep the response short and direct, no more than {max_length} characters.
2. Match the response to the requested tone/mode:
   - "brutal": extremely harsh, exposes the truth with no mercy.
   - "philosophical": honest with a deep, reflective lesson; makes the user think.
   - "sarcastic": sarcastic or witty, mixes truth with humor or light mockery.
3. Do not use highly offensive language or direct insults that could get the bot banned.
4. Make the response clear, engaging, and impactful according to the mode.
5. Focus only on the user's message; do not add greetings or extra commentary.

User's message: {user_message}

Respond ONLY with the final text, short, shocking, and matching the requested mode: {mode}. No explanations, no extra text."""