"""Module to create Connection class"""
from PyNodeEditor.core.nodeLogger import get_node_logger
from PyNodeEditor.core.registry import RegisterConnection

logger = get_node_logger(__file__)


@RegisterConnection
class Connection(object):
    """Creating a Connection class"""
    def __init__(self, **kwargs):
        """
        Initializing Connection class.
        Args:
            **kwargs (**kwargs): Keyword arguments of this class.
        """
        self._source_plug = kwargs.get("source_plug")
        self._destination_plug = kwargs.get("destination_plug")
        self._source_node = self._source_plug.node
        self._destination_node = self._destination_plug.node
        self._node_type = 'connection'
        self._destination_plug.value = self._source_plug.value

    def __repr__(self):
        """Presentation of this class"""
        return f'Connection({self._source_node.name}.{self._source_plug.name}'\
               f',{self.destination_node.name}.{self._destination_plug.name})'

    def __str__(self):
        """String representation of this class."""
        return f'Connection({self._source_node.name}.{self._source_plug.name}'\
               f',{self.destination_node.name}.{self._destination_plug.name})'

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
    def name(self):
        return self.__str__()

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
