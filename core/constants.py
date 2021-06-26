"""Module to declare all global variables"""
from network import Network
from nodeLogger import get_node_logger

logger = get_node_logger(__file__)

NETWORK = Network(name="root")


class NameCheck:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        node_name = args[0]
        if NETWORK.node_exists(node_name):
            logger.error(f'Failed to rename node "{node_name}", Please choose different name!')
            raise NameError(f'Failed to rename node "{node_name}", Please choose different name!')
        self.function(*args, **kwargs)
