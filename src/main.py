import logging

from src.explore import explore
from src.logging_conf import setup_logging
from src.settings import config

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    setup_logging()
    print(f"Environment Log Level: {config.LOG_LEVEL}")
    explore()
