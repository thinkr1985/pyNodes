"""Module to declare all global variables"""
import os
import logging
import tempfile

from core.network import Network

NETWORK = Network(name="root")
DEBUG_LEVEL = logging.DEBUG
TEMP_DIR = os.path.join(tempfile.gettempdir(), "NodeEditor")
