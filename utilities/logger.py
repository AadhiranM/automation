import logging
import os
from datetime import datetime

# Create logs folder if not exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file name (per run)
LOG_FILE = os.path.join(LOG_DIR, f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()   # also print to console
    ]
)

logger = logging.getLogger("AutomationLogger")
