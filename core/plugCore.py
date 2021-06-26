"""Module to create Plug class"""
import logging

from nodeLogger import get_node_logger

logger = get_node_logger(__file__)


class Plug:
    """This is a base class of all Plugs"""
    def __init__(self, node, name: str, value, **kwargs):
        """
        Initializing Plug class.
        Args:
            node (Node): Node for which attribute is made.
            name (str): Name of the plug.
            value (any): Value of the plug.
        """
        logger.debug(f'Initializing Plug "{name}" from the node "{node.name}"')

        self._node = node
        self._name = str(name)
        self._value = value
        self._keys = {0: self._value}

    def __repr__(self):
        """
        Representation of this class.
        Returns:
            str: Returns string representation of this class.
        """
        return f'Plug({self._name},{self.value}, {self._node.name})'

    def __str__(self):
        """
        String representation of the class.
        Returns:
            str: Returns string representation.
        """
        return f'Plug({self._name},{self.value}, {self._node.name})'

    def __iter__(self):
        """
        iter method of this class.
        Returns:
            dict: returns dictionary.
        """
        yield 'name', self._name
        yield 'value', self._value
        yield 'keys', self._keys
        yield 'isAnimated', self.is_animated

    def _dict(self):
        """
        Directory representation of this class.
        Returns:
            dict: Returns dict containing name, default value and keys.
        """
        return {'name': self._name,
                'value': self._value,
                'keys': self._keys,
                'isAnimated': self.is_animated}

    def as_dict(self):
        """
        This method converts casts this class to dict object.
        Returns:
            dict: Returns dictionary presentation of this class.
        """
        return self._dict()

    @property
    def node(self):
        return self._node

    @property
    def name(self):
        """
        creating a name property for this class.
        Returns:
            str: Returns name of the class.
        """
        return self._name

    @property
    def plug_type(self):
        """
        creating a plug_type property.
        Returns:
            type(self.value): returns type of the plug.
        """
        return type(self.value)

    @property
    def value(self):
        """
        Creating value property for the class.
        Returns:
            self.plug_type: returns the default value of the class.
        """
        return self._keys.get(0)

    @value.setter
    def value(self, value):
        """
        This method sets value for the class.
        Args:
            value (self.plug_type): Value for the plug.

        Returns:
            None: Returns None.
        """
        if self._value == value:
            return
        logger.info(f'setting {self.name} s value to {value}')
        self._value = value
        self._keys.update({0: value})

        if self != self._node.output_plug:
            self._node.evaluate()
        elif self == self._node.output_plug:
            self._node.evaluate_children()

    @property
    def keys(self):
        """Creating keys property
        Returns:
            dict: Returns keys of the plug.
        """
        return self._keys

    def get_key_value(self, frame_number: int):
        """
        This method gets the value of key at given frame number.
        Args:
            frame_number (int): Frame number in integer format.

        Returns:
            self.plug_type: returns value at the frame.
        """
        if not isinstance(frame_number, int):
            logger.error(msg='Frame number should of type "int" to get key value')
            raise TypeError
        logging.debug(f'Getting key value on frame {frame_number} from plug "{self._node.name}.{self._name}"')
        return self._keys.get(frame_number)

    def set_key(self, frame_number: int, value):
        """
        This method sets a key on given frame number and value.
        Args:
            frame_number (int): Frame number in integer format.
            value (type(self.plug_type): value at given frame.

        Returns:
            None: Returns None.
        """
        if not isinstance(frame_number, int):
            logger.error(msg='Frame number should of type "int" to set key')
            raise TypeError

        if not isinstance(value, self.plug_type):
            logger.error(
                msg=f'Failed to set key as given value is not of {self.plug_type} type.'
            )
            raise TypeError
        if not value:
            value = self.value
        logger.debug(
            f'Setting key on plug "{self._node.name}.{self._name}" on frame {frame_number} with value "{value}"'
        )
        self._keys.update({frame_number: value})

    def remove_key(self, frame_number: int):
        """
        This method removes key frame value at given frame number.
        Args:
            frame_number (int): Frame number in integer.

        Returns:
            None: Returns None.
        """
        if not isinstance(frame_number, int):
            logger.error(msg='Frame number should of type "int" to remove key')
            raise TypeError
        if frame_number in self._keys:
            logger.debug(f'Removing key on plug "{self._node.name}.{self._name}" on frame {frame_number}')
            self._keys.pop(frame_number)

    @property
    def is_animated(self):
        """
        This property return True if this plug has any keys on it.
        Returns:
            bool: Returns True if keyed else returns False.
        """
        if len(self._keys) > 1:
            return True

    def is_keyed_at_frame(self, frame_number: int):
        """
        This method checks if plug is keyed at given frame.
        Args:
            frame_number (int): Frame number.

        Returns:
            bool: Return True if its keyed else False.
        """
        if self.get_key_value(frame_number):
            return True


class InputPlug(Plug):
    """Creating InputPlug class by inheriting Plug"""
    def __init__(self, node, name: str, value, **kwargs):
        """
        Initializing InputPlug class.
        Args:
            node (Node): Parent Node object.
            name (str): Name of the Plug.
            value (Any): Value of the plug.
            **kwargs (Any): Any parameters which needs to pass to this class.
        """
        super(InputPlug, self).__init__(node=node, name=name, value=value, **kwargs)
        self._connection = None

    def __repr__(self):
        """Representation of this class."""
        return f'InputPlug({self._name},{self.value}, {self._node.name})'

    def __str__(self):
        """String representation of the class."""
        return f'InputPlug({self._name},{self.value}, {self._node.name})'

    @property
    def is_connected(self):
        """
        Checks if this plug is connected.
        Returns:
            bool: Returns True if its connected.
        """
        if self._connection:
            return True

    @property
    def connection(self):
        """
        Gets the connection object from this plug.
        Returns:
            Connection: Returns the connection object.
        """
        return self._connection

    def add_connection(self, connection_object):
        """
        Adds connection to this plug.
        Args:
            connection_object (Connection): Connection object.

        Returns:
            None: Returns None.
        """
        logger.debug(f'Connecting plug "{connection_object.source_node.name}.{connection_object.source_plug.name}" to "'
                     f'"{self.node.name}.{self.name}"')
        self._connection = connection_object

    def disconnect_plug(self):
        """
        This function disconnects the plug from any connection.
        Returns:
            bool: Returns True if disconnected else False.
        """
        if self._connection:
            logger.info(f'Disconnecting "{self.node.name}.{self.name}" from "{self._connection.source_node.name}.'
                        f'{self._connection.source_plug.name}"')
            self._connection = None
            self._node.evaluate()
            return True

        else:
            logger.error(f'There is no connections in plug '
                         f'"{self._node.name}.{self._name}" to disconnect.')
            return False


class OutputPlug(Plug):
    """Creating OutputPlug class by inheriting Plug"""
    def __init__(self, node, name: str, value, **kwargs):
        """
        Initializing OutPutPlug class.
        Args:
            node (Node): Parent Node object.
            name (str): Name of the Plug.
            value (Any): Value of the plug.
            **kwargs (Any): Any parameters which needs to pass to this class.
        """
        super(OutputPlug, self).__init__(node=node, name=name, value=value, **kwargs)
        self._connections = None

    def __repr__(self):
        """Representation of this class."""
        return f'OutputPlug({self._name},{self.value}, {self._node.name})'

    def __str__(self):
        """String representation of the class."""
        return f'OutputPlug({self._name},{self.value}, {self._node.name})'

    def set_key(self, frame_number: int, value):
        """Disabling set key functionality on OutPutPlug"""
        logger.error("Cannot set key on output type plug!")

    @property
    def connections(self):
        """
        Gets all the connections of this plug
        Returns:
            list: returns list containing all the connection object.
        """

        return self._connections

    @property
    def is_connected(self):
        """
        Checks if this plug is connected.
        Returns:
            bool: Returns True if its connected else returns False.
        """
        if self._connections:
            return True

    def add_connection(self, connection_object):
        """
        Adds the connection to this plug
        Args:
            connection_object (Connection): Connection object to add to this plug.

        Returns:
            None: Returns None.
        """
        for con in self._connections:
            if con.source_plug.name == self.name:
                logger.error(f'Failed to connect, connection from "{connection_object.source_node.name}'
                             f'.{connection_object.source_plug.name}" already exists in the plug "{self.node.name}.'
                             f'{self.name}"')
                raise ConnectionError
            else:
                logger.debug(f'Connecting to plug "{self.node.name}.{self.name}" to "'
                             f'{connection_object.destination_node.name}.{connection_object.destination_plug.name}"')
                self._connections.append(connection_object)

    def disconnect_plug(self, connection_object):
        """
        This function disconnects the plug from any connection.
        Args:
            connection_object (Connection): Connection object to remove.
        Returns:
            bool: Returns True if disconnected else False.
        """
        if self._connections:
            index = None
            for num, con in enumerate(self._connections):
                if con == connection_object:
                    index = num
                    break
            if index or index == 0:
                logger.info(f'Disconnecting "{self.node.name}.{self.name}" from "'
                            f'{connection_object.destination_node.name}.{connection_object.destination_plug.name}"')
                self._connections.pop(index)
                self._node.evaluate_children()
                return True
            else:
                logger.error(f'Failed to remove connection from "{self.node.name}.{self.name}"')

        else:
            logger.error(f'Failed to remove connection from "{self.node.name}.{self.name}"')
