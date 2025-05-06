import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, "api.log")

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=5_000_000, backupCount=5, encoding='utf-8')
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(handler)