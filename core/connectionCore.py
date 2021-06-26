"""Module to create Connection class"""
from nodeLogger import get_node_logger
from constants import NETWORK

logger = get_node_logger(__file__)


class Connection:
    """Creating a Connection class"""
    def __init__(self, source_plug, destination_plug, **kwargs):
        """
        Initializing Connection class.
        Args:
            source_plug (OutputPlug): Source plug of the connection.
            destination_plug (InputPlug): Destination plug of the connection.
            **kwargs (**kwargs): Keyword arguments of this class.
        """
        if not source_plug.node_type == destination_plug.node_type:
            logger.error(f'Connection cant be made in between "{source_plug.node.name}.{source_plug.name}" and '
                         f'"{destination_plug.node.name}.{destination_plug.name}"'
                         f'as both have different types')
            raise TypeError

        logger.debug(f'Creating connection from "{source_plug.node.name}.{source_plug.name}"'
                     f' to "{destination_plug.node.name}.{destination_plug.name}"')

        self._source_node = source_plug.node
        self._destination_node = destination_plug.node
        self._source_plug = source_plug
        self._destination_plug = destination_plug

        self._source_plug.add_connection(self)
        self._destination_plug.connection = self
        self._node_type = 'connection'

    def __repr__(self):
        """Presentation of this class"""
        return f'Connection({self._source_node.name}.{self._source_plug.name},' \
               f'{self.destination_node.name}.{self._destination_plug.name})'

    def __str__(self):
        """String representation of this class."""
        return f'Connection({self._source_plug.name},{self._destination_plug.name})'

    def __iter__(self):
        """
        Creating iterator for this class.
        Returns:
            dict: Returns dict.
        """
        yield 'sourcePlug', self._source_plug.name
        yield 'destinationPlug', self._destination_plug.name
        yield 'sourceNode', self._source_node.name
        yield 'destinationNode', self._destination_node.name

    def _dict(self):
        """
        This private converts class to dictionary.
        Returns:
            dict: returns class dict.
        """
        return {
            'sourcePlug': self._source_plug.name,
            'destinationPlug': self._destination_plug.name,
            'sourceNode': self._source_node.name,
            'destinationNode': self._destination_node.name
        }

    def as_dict(self):
        """
        This method gets this class in dictionary format.
        Returns:
            dict: Returns dict.
        """
        return self._dict()

    @property
    def node_type(self):
        return self._node_type

    @property
    def source_plug(self):
        """This property gets the source plug object of this connection"""
        return self._source_plug

    @property
    def destination_plug(self):
        """This property gets the destination plug of this connection"""
        return self._destination_plug

    @property
    def destination_node(self):
        """This property gets the destination node of this connection"""
        return self._destination_node

    @property
    def source_node(self):
        """This property gets source node of this connection"""
        return self._source_node
