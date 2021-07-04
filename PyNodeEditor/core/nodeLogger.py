"""Creating a Logger module"""
import os
import logging
import datetime
import tempfile

APP_NAME = "NodeEditor"
DEBUG_LEVEL = logging.DEBUG
TEMP_DIR = os.path.join(tempfile.gettempdir(), APP_NAME)

DATESTAMP = datetime.datetime.now().strftime("%d-%b-%Y")
LOG_FILE = os.path.join(TEMP_DIR, f"{DATESTAMP}.log")


def get_node_logger(module=__file__, debug_level=logging.DEBUG):
    """
    This function creates a logger with given arguments.
    Args:
        module (str): string to use as name of logger.
        debug_level (logging.DEBUG): Debug Level of the logger.

    Returns:
        logging.getLogger: Returns the logger object.
    """
    if not debug_level:
        debug_level = DEBUG_LEVEL

    if not module:
        module = __file__

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    logger_name = os.path.split(module)[-1].split(".")[0]
    formatter = logging.Formatter(
        fmt='%(levelname)s\t%(asctime)s-%(name)s-%(funcName)s-\t%(message)s',
        datefmt='%d-%b-%y-%H:%M:%S'
    )

    log_stream_handler = logging.StreamHandler()
    log_stream_handler.setFormatter(formatter)
    log_stream_handler.setLevel(debug_level)

    log_file_handler = logging.FileHandler(LOG_FILE)
    log_file_handler.setFormatter(formatter)
    log_file_handler.setLevel(logging.DEBUG)

    node_logger = logging.getLogger(logger_name)
    node_logger.addHandler(log_file_handler)
    node_logger.addHandler(log_stream_handler)
    node_logger.setLevel(debug_level)

    return node_logger
