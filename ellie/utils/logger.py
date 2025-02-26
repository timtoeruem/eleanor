import logging
from ellie.utils.config import ConfigManager

class LogManager(ConfigManager):
    def __init__(self, config=None):
        super().__init__()
        self.logger = logging.getLogger("Ellie")
        self.handler = logging.FileHandler("logs.log")
        self.formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s: %(message)s")
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)