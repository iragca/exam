import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

BACKEND_CONFIG = PROJECT_ROOT / "backend" / "config.py"

# Check if .env file exists and load it
if not (PROJECT_ROOT / ".env").exists():
    logger.error("No .env file found in the project root.")

# Check if DATABASE_URL is set in the environment variables
if DATABASE_URL is None:
    logger.error("DATABASE_URL wasn't found in the environment variables.")

logger.info(f"Project root: {PROJECT_ROOT}")
logger.info(f"Backend config path: {BACKEND_CONFIG}")
