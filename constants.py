"""Module to declare all global variables"""
import os
import logging
import tempfile


DEBUG_LEVEL = logging.DEBUG
TEMP_DIR = os.path.join(tempfile.gettempdir(), "NodeEditor")
