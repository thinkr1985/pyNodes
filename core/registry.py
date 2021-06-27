"""This module contains all the registry classes"""
from constants import NETWORK
from nodeLogger import get_node_logger

logger = get_node_logger(__file__)


class NameCheck:
    """Creating a NameCheck decorator class.
        Calling this class as decorator to your node rename functions makes sure
        that the node you are renaming have a unique name inside the network.
    """
    def __init__(self, function):
        self._function = function

    def __call__(self, *args, **kwargs):
        node_name = args[0]
        if NETWORK.node_exists(node_name):
            logger.error(f'Failed to rename node "{node_name}", Please choose different name!')
            raise NameError(f'Failed to rename node "{node_name}", Please choose different name!')
        self._function(*args, **kwargs)


class RegisterConnection:
    """Creating RegisterConnection decorator class.
        Calling this class as decorator to your connection object validates the
        plugs before you create the class and adds the connection to the network.
    """
    def __init__(self, connection_class):
        self._connection_class = connection_class

    def __call__(self, **kwargs):
        source_plug = kwargs.get("source_plug")
        destination_plug = kwargs.get("destination_plug")

        if not source_plug or not destination_plug:
            logger.error('Failed to create connection, "source_plug" or "destination_plug" not provided!')
            raise KeyError("source_plug or destination_plug not given to create connection")

        connection = self._connection_class(**kwargs)
        logger.debug(f'Registering connection "{connection.name}" to network "{NETWORK.name}"')
        NETWORK.add_connection(connection)


class DeRegisterConnection:
    """Creating DeRegisterConnection decorator class.
        Calling this class as decorator before your disconnect function on node makes sure
        to remove it from network.
    """
    def __init__(self, connection_class):
        self._connection_class = connection_class

    def __call__(self, **kwargs):
        pass


class RegisterNode:
    """Creating RegisterNode decorator class.
        Calling this class as decorator to Node class makes sure the node with
        same name does not exists in the network and adds the resulting node to the network.
    """
    def __init__(self, node_class):
        self._node_class = node_class

    def __call__(self, **kwargs):
        name = kwargs.get("name")
        if not name:
            logger.error('Failed to register node without a name!')
            raise NameError('Failed to register node without a name!')

        if NETWORK.node_exists(name):
            logger.error(f'Failed to register node "{name}" as node with same name already exists!')
            raise NameError(f'Failed to register node "{name}" as node with same name already exists!')

        logger.debug(f'Registering node "{name}" to network "{NETWORK.name}"')
        node = self._node_class(**kwargs)
        NETWORK.add_node(node)


class RegisterInputPlug:
    """Creating a RegisterInputPlug decorator class.
        Calling this class as decorator your InputPlug class makes sure its
        unique and adds the plug to node and network.
    """
    def __init__(self, input_plug_class):
        self._input_plug_class = input_plug_class

    def __call__(self, **kwargs):
        name = kwargs.get("name")
        node = kwargs.get("node")
        value = kwargs.get("value")

        if not name or not node or not value:
            logger.error('Failed to register plug without a name/node/value!')
            raise NameError('Failed to register plug without a name/node/value!')

        if node.get_plug(name):
            logger.error(f'Failed to register plug to node "{node.name}" as plug with same name already exists!')
            raise NameError

        plug = self._input_plug_class(**kwargs)
        logger.debug(f'Registering Plug "{node.name}.{name}" to node "{node.name}"')
        node.add_plug(plug)
