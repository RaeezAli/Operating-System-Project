import logging
import os
from datetime import datetime

class JarvisLogger:
    """
    Centralized logging system for Jarvis OS Simulator.
    Follows point 6: Proper logging and error handling.
    """
    
    def __init__(self, name="Jarvis"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Avoid duplicate handlers
        if not self.logger.handlers:
            # Console Handler
            ch = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)
            
            # File Handler
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            fh = logging.FileHandler(os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log"))
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg, exc_info=True):
        self.logger.error(msg, exc_info=exc_info)

    def warning(self, msg):
        self.logger.warning(msg)

# Singleton global logger
logger = JarvisLogger()