import logging
import sys

LOG_FORMAT = "[%(asctime)s] %(levelname)s - %(message)s"

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger