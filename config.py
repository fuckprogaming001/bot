import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# Load environment variables from .env file
load_dotenv()

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")

# Telegram Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID")) if os.getenv("API_ID") else None
API_HASH = os.getenv("API_HASH")

# Admin and Security Configuration
ADMIN_USER_IDS = [int(os.getenv("ADMIN_ID"))] if os.getenv("ADMIN_ID") else []
TWO_FA_PASSWORD = os.getenv("TWO_FA_PASSWORD")

# Directories (will create if missing)
SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

# --- Spam check configuration ---
SPAM_CHECK_STATUS_FILE = "spam_check_status.txt"

def is_spam_check_enabled() -> bool:
    """Reads the spam check status from file and returns True if enabled."""
    try:
        if not os.path.exists(SPAM_CHECK_STATUS_FILE):
            # If file doesn't exist, default to 'on'
            with open(SPAM_CHECK_STATUS_FILE, "w") as f:
                f.write("on")
            return True
        
        with open(SPAM_CHECK_STATUS_FILE, "r") as f:
            status = f.read().strip().lower()
            return status == "on"
    except Exception:
        return True  # Default to enabled if any error occurs

# Channel Configuration
REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", "@JB_TEAMRECHIVERBOTUPTED")
WITHDRAW_CHANNEL_ID = int(os.getenv("WITHDRAW_CHANNEL_ID", -1003081412669))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", -1002770556868))
LOG_CHANNEL_USERNAME = os.getenv("LOG_CHANNEL_USERNAME", "@User_Number_Chek")

# Join Channel Button
join_button = InlineKeyboardButton(
    text="Join Our Channel",
    url=f"https://t.me/{REQUIRED_CHANNEL.strip('@')}"
)

# Keyboard creation
keyboard = InlineKeyboardMarkup([[join_button]])
