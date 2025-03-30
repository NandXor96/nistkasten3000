import os
import glob
import logging
import config

# Logging Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(f"{config.BOT_NAME}")
logger.setLevel(logging.INFO)

# Andere Logger auf WARNING setzen
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('apscheduler').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)

def log(message: str, level: str = "INFO") -> None:
    log_level = getattr(logging, level.upper())
    logger.log(log_level, message)

def log_error(message: str, error: Exception) -> None:
    log(f"{message}: {str(error)}", "ERROR") 

def del_file(file):
    if config.DELETE_FILES:
        try:
            os.remove(file)
        except Exception as e:
            log_error(f"Error deleting file {file}", e)

def cleanup_media_directory():
    if config.DELETE_FILES:
        for file in glob.glob(f"{config.MEDIA_DIR}/*"):
            del_file(file)
        log("Cleaned up media directory")