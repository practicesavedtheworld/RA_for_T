import logging
import sys


def create_logger(loger_name: str, file_name: str = None, level: int = 10):
    """Create logger. Default prints all info into console."""

    logger = logging.getLogger(loger_name)
    logger.setLevel(level)

    logger_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    if file_name:
        handler = logging.FileHandler(filename=file_name if file_name else __file__, encoding='UTF-8')
    else:
        handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logger_formatter)
    handler.setLevel(level)

    logger.addHandler(handler)

    return logger
