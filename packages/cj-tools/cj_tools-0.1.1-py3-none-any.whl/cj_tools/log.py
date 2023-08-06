import os
import logging
from logging.handlers import TimedRotatingFileHandler


class LoggerFactory(object):
    os.makedirs("log", exist_ok=True)
    _LOG_FILE = "log/standard.log"
    _LOG_FORMAT = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s"
    _logger = logging.getLogger("CJ")
    _logger.setLevel(level=logging.DEBUG)
    _formatter = logging.Formatter(_LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')


    _console = logging.StreamHandler()
    _console.setLevel(logging.INFO)
    _logger.addHandler(_console)

    _handler = TimedRotatingFileHandler(_LOG_FILE, when='D', interval=1, backupCount=14, encoding="UTF-8", delay=True)
    _handler.setFormatter(_formatter)
    _logger.addHandler(_handler)

    @staticmethod
    def set_log_file(log_file: str = None):
        if log_file is not None:
            LoggerFactory._logger.removeHandler(LoggerFactory._handler)
            handler = TimedRotatingFileHandler("log/" + log_file, when='D', interval=1, backupCount=14,
                                               encoding="UTF-8", delay=True)
            handler.setFormatter(LoggerFactory._formatter)
            LoggerFactory._logger.addHandler(handler)

    @staticmethod
    def set_level_display(Level: int = None):
        if Level is not None:
            LoggerFactory._console.setLevel(Level)

    @staticmethod
    def get_logger():
        return LoggerFactory._logger