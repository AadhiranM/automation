import logging
import os

# Log folder
LOG_DIR = "reports/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Single reusable log file
LOG_FILE = f"{LOG_DIR}/automation.log"

# Create logger
logger = logging.getLogger("automation")
logger.setLevel(logging.INFO)

# Avoid duplicate handlers
if not logger.handlers:

    # -------------------------
    # FILE HANDLER (one file only)
    # -------------------------
    file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    file_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # -------------------------
    # CONSOLE HANDLER (terminal)
    # -------------------------
    console_handler = logging.StreamHandler()
    console_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

logger.info("📘 Logger initialized — writing to automation.log")
