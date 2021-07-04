"""Creating Network class"""
from nodeLogger import get_node_logger

logger = get_node_logger(__file__)


class Network(object):
    """Creating a Network class"""
    def __init__(self, **kwargs):
        """
        Initializing Network class.
        Args:
            **kwargs: keyword arguments of this class.
        """
        self._node_type = 'network'
        self._name = kwargs.get('name') or str()
        self._nodes = dict()
        self._connections = dict()
        self._plugs = dict()

    def __repr__(self):
        """Representing this class"""
        return f'Network() at {hex(id(self))}'

    def __str__(self):
        """Representing this class in string format"""
        return f'Network()'

    def __iter__(self):
        """
        Creating iterator for this class.
        Returns:
            dict: Returns dict representation of this class.
        """
        yield 'nodes', self._nodes
        yield 'connections', self._connections

    def _dict(self):
        """
        This method casts this class into dictionary.
        Returns:
            dict: returns dictionary.
        """
        return {
            'nodes': self._nodes,
            'connections': self._connections
        }

    def as_dict(self):
        """
        converts this class into dictionary.
        Returns:
            dict: Returns dictionary containing network data.
        """
        return self._dict()

    @property
    def name(self):
        """
        This property returns name of this class.
        Returns:
            str: return class name.
        """
        return self._name

    @property
    def node_type(self):
        """
        This property returns type of this class.
        Returns:
            str: returns class type.
        """
        return self._node_type

    @property
    def nodes(self):
        """
        This property returns all nodes present in the network.
        Returns:
            dict: returns dictionary containing node data.
        """
        return self._nodes

    @property
    def connections(self):
        """
        This property returns all the connection present in the network.
        Returns:
            dict: returns dictionary containing connection data.
        """
        return self._connections

    @property
    def plugs(self):
        """
        This property returns all the plugs present in the network.
        Returns:
            dict: returns dictionary containing plugs data.
        """
        return self._plugs

    def connection_exists(self, connection_object):
        """
        This method checks if given connection object presents in the network.
        Args:
            connection_object: Connection object.

        Returns:
            bool: returns True if connection is present in network
             else returns False.
        """
        if connection_object.name in self._connections:
            return True

    def node_exists(self, node_name: str):
        """
        This method checks if given node with name present in the network.
        Args:
            node_name (str): Name of the node to check.

        Returns:
            bool: Returns True if node with this present in the network.
        """
        for node_type, nodes in self._nodes.items():
            for node in nodes:
                if node.name == node_name:
                    return True

    def add_node(self, node):
        """
        This method adds given node to network.
        Args:
            node: Node Object.

        Returns:
            bool: Returns True of node gets added to network.
        """
        if self.node_exists(node.name):
            raise NameError(
                f'Failed to add node with name "{node.name}",'
                f' Please choose different name!'
            )
        node_type = node.node_type
        logger.debug(
            f'Adding node node "{node.name}" to Network "{self._name}"'
        )

        if node_type in self._nodes:
            nodes = self._nodes[node_type]
            nodes.append(node)
            self._nodes[node_type] = nodes
            return True
        else:
            self._nodes.update({node_type: [node]})
            return True

    def add_plug(self, plug_object):
        """
        This method adds given plug object to the network.
        Args:
            plug_object: Plug object.

        Returns:
            bool: Returns True if it successfully adds the plug.
        """
        self._plugs.update({plug_object.name: plug_object})
        return True

    def add_connection(self, connection_object):
        """
        This method adds the given connection object the network.
        Args:
            connection_object: Connection object.

        Returns:
            bool: Returns True if it successfully adds connection to network.
        """
        self._connections.update({connection_object.name: connection_object})
        return True

    def unregister_connection(self, connection_object):
        """
        This method un registers the connection object from the network.
        Args:
            connection_object: conection object.

        Returns:
            bool: Returns True if it successfully unregisters the connection.
        """
        if connection_object.name in self._connections:
            logger.debug(
                f'Unregistering connection "{connection_object.__str__}" '
                f'from network "{self._name}"'
            )
            self._connections.pop(connection_object.name)
            return True
