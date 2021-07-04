"""This module contains all the custom exception classes"""
from nodeLogger import get_node_logger

logger = get_node_logger(__file__)


class ConnectionCreationError(Exception):
    """Get raised when connection creation fails."""
    def __init__(self, message=None):
        super().__init__()
        logger.error(message)


class NodeRegistrationError(Exception):
    """Gets raised when failed to register a node"""
    def __init__(self, message=None):
        super().__init__()
        logger.error(message)


class PlugRegistrationError(Exception):
    """Gets raised when plug is failed to register"""
    def __init__(self, message=None):
        super().__init__()
        logger.error(message)


class GroupRegistrationError(Exception):
    """Gets raised when group is failed to register"""
    def __init__(self, message=None):
        super().__init__()
        logger.error(message)


class ComputeError(Exception):
    """Get raised when node fails to compute"""
    def __init__(self, message=None):
        super().__init__()
        logger.error(message)


class NetworkOpenError(Exception):
    """Get raised when engine fails to load / open network from file."""
    def __init__(self, message=None):
        super().__init__()
        logger.error(message)


class MissingPlugError(Exception):
    """Get raised when failed to found the plug."""
    def __init__(self, message=None):
        super().__init__()
        logger.error(message)
