import logging
import os
import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

LOG_DIR = os.path.join(
    PROJECT_ROOT,
    "reports",
    "logs"
)
# -------------------------
# LOG PATH SETUP
# -------------------------
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = f"{LOG_DIR}/automation.log"

# -------------------------
# CREATE LOGGER
# -------------------------
logger = logging.getLogger("automation")
logger.setLevel(logging.INFO)
logger.propagate = False

# 🔥 IMPORTANT: Remove existing handlers (pytest reuse issue)
if logger.hasHandlers():
    logger.handlers.clear()

# -------------------------
# FILE HANDLER (OVERWRITE)
# -------------------------
file_handler = logging.FileHandler(
    LOG_FILE,
    mode="w",              # ✅ overwrite every run
    encoding="utf-8"
)
file_format = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

# -------------------------
# CONSOLE HANDLER
# -------------------------
console_handler = logging.StreamHandler()
console_format = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

logger.info("📘 Logger initialized — fresh run, old logs cleared")
