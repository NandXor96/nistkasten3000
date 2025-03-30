import os
from language import language
    
# Bot configuration
BOT_NAME: str = os.getenv("BOT_NAME", "Nistkasten 3000")
BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "0")
CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "0")
CHAT_TIMEOUT: float = float(os.getenv("TELEGRAM_TIMEOUT", "20")) # Timeout for Telegram API requests

# Media configuration
VIDEO_DURATION: int = int(os.getenv("VIDEO_DURATION", "30")) # For manual video recording

# File Management
DELETE_FILES: bool = os.getenv("DELETE_FILES", "True").lower() == "true"

# Language
LANGUAGE: str = os.getenv("LANGUAGE", "en") # Language for the bot

if LANGUAGE not in language:
    LANGUAGE = "en"

# Message configuration
VIDEO_MESSAGE: str = language[LANGUAGE]["video_message"]
PHOTO_MESSAGE: str = language[LANGUAGE]["photo_message"]
ERROR_MESSAGE: str = language[LANGUAGE]["error_message"]
START_VIDEO_MESSAGE: str = language[LANGUAGE]["start_video_message"]
ACTIVATED: str = language[LANGUAGE]["activated"]
DEACTIVATED: str = language[LANGUAGE]["deactivated"]
MOTION_DETECTION_IS: str = language[LANGUAGE]["motion_detection_is"]

# Motion configuration
WEB_URL: str = "http://localhost:8080"
MEDIA_DIR: str = "/media"

def validate() -> None:
    """Überprüft die Konfiguration auf Gültigkeit"""
    if not BOT_TOKEN or BOT_TOKEN == "0":
        raise ValueError("TELEGRAM_BOT_TOKEN must be set")
    if not CHAT_ID or CHAT_ID == "0":
        raise ValueError("TELEGRAM_CHAT_ID must be set")
    if not os.path.exists(MEDIA_DIR):
        raise ValueError(f"MEDIA_DIR {MEDIA_DIR} does not exist")
    if VIDEO_DURATION < 10:
        raise ValueError("VIDEO_DURATION must be greater than 10")
    if CHAT_TIMEOUT < 5:
        raise ValueError("CHAT_TIMEOUT must be greater than 5")
    if LANGUAGE not in language:
        raise ValueError(f"LANGUAGE {LANGUAGE} is not supported")