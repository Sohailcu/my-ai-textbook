import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger(name: str, log_file: str, level=logging.INFO):
    """Function to setup a logger with file and console handlers"""
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, log_file),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Create loggers for different components
app_logger = setup_logger('app_logger', 'app.log')
rag_logger = setup_logger('rag_logger', 'rag.log')
auth_logger = setup_logger('auth_logger', 'auth.log')