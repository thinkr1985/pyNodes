"""Module to declare all global variables"""
from network import Network
from nodeLogger import get_node_logger

logger = get_node_logger(__file__)

NETWORK = Network(name="root")
