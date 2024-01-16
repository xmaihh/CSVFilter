import logging


class MyLogger:
    def __init__(self, name, log_file):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        mode = "a" if self.logger.handlers else "w"

        file_handler = logging.FileHandler(log_file, mode=mode)
        file_handler.setLevel(logging.DEBUG)

        screen_handler = logging.StreamHandler()
        screen_handler.setLevel(logging.DEBUG)

        self.log_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler.setFormatter(self.log_formatter)
        screen_handler.setFormatter(self.log_formatter)

        self.logger.handlers = []

        self.logger.addHandler(file_handler)
        self.logger.addHandler(screen_handler)

    def get_logger(self):
        return self.logger

    def get_log_formatter(self):
        return self.log_formatter

    def log_debug(self, message):
        self.logger.debug(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_critical(self, message):
        self.logger.critical(message)
