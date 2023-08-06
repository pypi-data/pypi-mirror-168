#!/usr/bin/env python
# coding: utf-8
from intelliw.config import config
import threading
import logging.handlers
import os

framework_logger = None
user_logger = None


class Logger():
    _instance_lock = threading.Lock()

    def __new__(cls):
        """ 单例,防止调用生成更多 """
        if not hasattr(Logger, "_instance"):
            with Logger._instance_lock:
                if not hasattr(Logger, "_instance"):
                    Logger._instance = object.__new__(cls)
        return Logger._instance

    def __init__(self):
        level = logging.INFO if config.is_server_mode else logging.DEBUG

        self.framework_logger = self._get_logger(
            "Framework Log", level=level, filename="iw-algo-fx.log")
        self.user_logger = self._get_logger(
            "Algorithm Log", level=level, filename="iw-algo-fx-user.log")

    def _get_logger(self, logger_type, level=logging.INFO, format=None, filename=None):
        logger = logging.getLogger(logger_type)
        if logger.handlers:
            return logger

        if not format:
            format = '[%(name)s] %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)s: %(message)s'

        logging.basicConfig(level=level, format=format,
                            datefmt='%Y-%m-%d %H:%M:%S')

        if filename is not None:
            log_path = './logs/'
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            if os.access(log_path, os.W_OK):
                time_file_handler = logging.handlers.TimedRotatingFileHandler(
                    os.path.join(log_path, filename),
                    when='D',
                    interval=2,
                    backupCount=180
                )
                format_object = logging.Formatter(
                    format, datefmt='%Y-%m-%d %H:%M:%S')
                time_file_handler.suffix = '%Y-%m-%d-%H.log'
                time_file_handler.setLevel(level)
                time_file_handler.setFormatter(format_object)
                logger.addHandler(time_file_handler)
        return logger


def _get_framework_logger():
    global framework_logger
    if framework_logger is None:
        framework_logger = Logger().framework_logger
    return framework_logger


def _get_algorithm_logger():
    global user_logger
    if user_logger is None:
        user_logger = Logger().user_logger
    return user_logger


def get_logger(name: str = "user", level: str = "INFO", format: str = None, filename: str = None):
    """get custom logs

    Args:
        name (str, optional): Logger unique name. Defaults to "user".
        level (str, optional): Logger level. Defaults to "INFO".
        format (str, optional): Format the specified record. Defaults to None.
        filename (str, optional): Save the name of the log file. Defaults to None.

    Returns:
        logger
    """
    return Logger()._get_logger(name, level, format, filename)
