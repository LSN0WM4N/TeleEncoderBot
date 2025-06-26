import os
import sys
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    os.makedirs('logs', exist_ok=True)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_handler = RotatingFileHandler(
        'logs/bot.log',
        maxBytes=5*1024*1024,  
        backupCount=3,         
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger

def remove_logs(): 
    os.remove('./logs/*.log')