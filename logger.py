import logging
from logging.handlers import TimedRotatingFileHandler
import sys

FORMATTER = logging.Formatter("[%(asctime)s] — %(levelname)s — [%(name)s %(filename)s.%(funcName)s:%(lineno)d] — %(message)s")
LOG_FILE = None
VERBOSE = False

def set_output(filename):
    global LOG_FILE
    LOG_FILE = filename

def set_verbose():
    global VERBOSE
    VERBOSE = True

def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler

def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE)
    file_handler.setFormatter(FORMATTER)
    return file_handler

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    if LOG_FILE:
        logger.addHandler(get_file_handler())
    if VERBOSE:
        logger.addHandler(get_console_handler())
    return logger
