import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure log directory exists
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Formatters
standard_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """Function to setup as many loggers as you want"""
    handler = RotatingFileHandler(os.path.join(LOG_DIR, log_file), maxBytes=10485760, backupCount=5)
    handler.setFormatter(standard_formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    # Prevent adding handlers multiple times in dev
    if not logger.handlers:
        logger.addHandler(handler)
        
        # Also log to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(standard_formatter)
        logger.addHandler(console_handler)

    return logger

# Setup individual loggers
app_logger = setup_logger('application', 'app.log')
prediction_logger = setup_logger('prediction', 'prediction.log')
error_logger = setup_logger('error', 'error.log', level=logging.ERROR)
