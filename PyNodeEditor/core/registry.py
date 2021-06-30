"""This module contains all the registry classes"""
from functools import update_wrapper, partial

import constants
from nodeLogger import get_node_logger

logger = get_node_logger(__file__)


class NameCheck(object):
    """Creating a NameCheck decorator class.
        Calling this class as decorator to your node rename functions makes sure
        that the node you are renaming have a unique name inside the network.
    """
    def __init__(self, function):
        update_wrapper(self, function)
        self._function = function

    def __get__(self, obj, obj_type):
        return partial(self.__call__, obj)

    def __call__(self, *args, **kwargs):
        node_name = args[0]
        if constants.NETWORK.node_exists(node_name):
            logger.error(f'Failed to rename node "{node_name}", Please choose different name!')
            raise NameError(f'Failed to rename node "{node_name}", Please choose different name!')
        self._function(*args, **kwargs)


class RegisterConnection(object):
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

        if f"{source_plug.node.name}.{source_plug.name}" == f"{destination_plug.node.name}.{destination_plug.name}":
            logger.error('Connection cant be made, source and destination plugs cant be same!')
            raise ConnectionError(f'Failed to create Connection in between "{source_plug.node.name}.'
                                  f'{source_plug.name}" and "{destination_plug.node.name}.{destination_plug.name}"')

        if source_plug.node_type == destination_plug.node_type:
            logger.error('Same type of plugs cant be connected.')
            raise TypeError(f'Failed to connect "{source_plug.node.name}.{source_plug.name}" to'
                            f' "{destination_plug.node.name}.{destination_plug.name}"')

        connection = self._connection_class(**kwargs)
        logger.debug(f'Registering connection "{connection.name}" to network "{constants.NETWORK.name}"')
        constants.NETWORK.add_connection(connection)
        source_plug.add_connection(connection)
        destination_plug.add_connection(connection)
        return connection


class DeRegisterConnection(object):
    """Creating DeRegisterConnection decorator class.
        Calling this class as decorator before your disconnect function on node makes sure
        to remove it from network.
    """
    def __init__(self, connection_class):
        self._connection_class = connection_class

    def __call__(self, **kwargs):
        pass


class RegisterNode(object):
    """Creating RegisterNode decorator class.
        Calling this class as decorator to Node class makes sure the node with
        same name does not exists in the network and adds the resulting node to the network.
    """

    def __init__(self, node_class):
        self._node_class = node_class

    def __get__(self, obj, obj_type):
        return partial(self.__call__, obj)

    def __call__(self, **kwargs):
        name = kwargs.get("name")
        if not name:
            logger.error('Failed to register node without a name!')
            raise NameError('Failed to register node without a name!')

        if constants.NETWORK.node_exists(name):
            logger.error(f'Failed to register node "{name}" as node with same name already exists!')
            raise NameError(f'Failed to register node "{name}" as node with same name already exists!')

        node = self._node_class(**kwargs)
        logger.debug(f'Registering node "{node.name}" to Network "{name}"')
        constants.NETWORK.add_node(node)
        return node


class RegisterInputPlug(object):
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

        if not name or not node or type(value) is None:
            logger.error('Failed to register plug without a name/node/value!')
            raise NameError('Failed to register plug without a name/node/value!')

        if node.get_plug(name):
            logger.error(f'Failed to register plug to node "{node.name}" as plug with same name already exists!')
            raise NameError

        plug = self._input_plug_class(**kwargs)
        logger.debug(f'Registering Plug "{node.name}.{name}" to node "{node.name}"')
        node.add_plug(plug)
        return plug
