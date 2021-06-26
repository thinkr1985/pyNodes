"""Creating Network class"""
from nodeLogger import get_node_logger

logger = get_node_logger(__file__)


class Network:
    def __init__(self, **kwargs):
        self._node_type = 'network'
        self._name = kwargs.get('name') or str()
        self._nodes = {}
        self._connections = []

    def __repr__(self):
        return f'Network()'

    def __str__(self):
        return f'Network()'

    def __iter__(self):
        yield 'nodes', self._nodes
        yield 'connections', self._connections

    def _dict(self):
        return {
            'nodes': self._nodes,
            'connections': self._connections
        }

    def as_dict(self):
        return self._dict()

    @property
    def name(self):
        return self._name

    @property
    def node_type(self):
        return self._node_type

    @property
    def nodes(self):
        return self._nodes

    @property
    def connections(self):
        return self._connections

    def node_exists(self, node_name: str):
        for node_type, nodes in self._nodes.items():
            for node in nodes:
                if node.name == node_name:
                    return True

    def register_node(self, node):
        if self.node_exists(node.name):
            raise NameError(f'Failed to register node name "{node.name}", Please choose different name!')
        node_type = node.node_type
        logger.debug(f'Registering node "{node.name}" to Network "{self._name}"')

        if node_type in self._nodes:
            nodes = self._nodes[node_type]
            nodes.append(node)
            self._nodes[node_type] = nodes
            return True
        else:
            self._nodes.update({node_type: [node]})
            return True

