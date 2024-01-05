import logging
import os


class MyLogger:
    def __init__(self, name, log_file):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 如果已有handler,则用追加模式，否则直接覆盖
        mode = "a" if self.logger.handlers else "w"

        # 创建文件处理程序,输出到文件
        file_handler = logging.FileHandler(log_file, mode=mode)
        file_handler.setLevel(logging.DEBUG)

        # 创建文本处理程序,输出到屏幕日志
        screen_handler = logging.StreamHandler()
        screen_handler.setLevel(logging.DEBUG)

        # 创建日志格式器
        self.log_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        # 将格式器添加到处理程序
        file_handler.setFormatter(self.log_formatter)
        screen_handler.setFormatter(self.log_formatter)

        # 清空已有的 handler
        self.logger.handlers = []

        # 将处理程序添加到日志记录器
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
