"""
Logging Utility Module
======================
Provide logging via console and log files.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class Log:
    """
    Logging Utility Class
    """
    def __init__(self, app_name: str, default_level: str = "info"):
        """
        Initialise logging class
        :param app_name: application name
        :param default_level: default logging level
        """
        self.app_name = app_name
        self.logger = logging.getLogger(app_name)
        self.default_level = self._get_level(default_level)
        self.logger.setLevel(self.default_level)

        fh = RotatingFileHandler(f"{Path(__file__).resolve().parent.parent.parent}/logs/{app_name}.log",maxBytes=10485760,backupCount=100)
        ch = logging.StreamHandler()

        self.formatter = logging.Formatter(
            fmt="{'timestamp': '%(asctime)s', 'bot': '%(name)s', 'level': '%(levelname)s', 'msg': '%(message)s'}",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        fh.setFormatter(self.formatter)
        ch.setFormatter(self.formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    @staticmethod
    def _get_level(level: str) -> int:
        """
        Get logging level
        :param level: loggin level
        :return: integer associated with level
        """
        valid_levels = {
            "CRITICAL": logging.CRITICAL,
            "ERROR": logging.ERROR,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
            "NOTSET": logging.NOTSET,
        }
        return valid_levels[level.upper()]

    def set_default_level(self, level: str | int):
        """
        Set default logging level
        :param level: loggin level
        :return: integer associated with level
        """
        if isinstance(level, str):
            level = self._get_level(level)
        self.logger.setLevel(level)
        self.default_level = level

    def write(self, message: str, level: str = None):
        """
        Write message to log file
        :param message: text message
        :param level: loggin level
        """
        log_level = self.default_level if level is None else self._get_level(level)
        self.logger.log(log_level, message)
