"""Module to declare all global variables"""
import os

from network import Network
from engine import Engine

APP_NAME = "NodeEditor"

NETWORK = Network(name="root")

ENGINE = Engine()

DEFAULT_NODES = {}

ICON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons")
