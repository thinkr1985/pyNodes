"""Creating Group class"""
from nodeLogger import get_node_logger
from constants import NETWORK

logger = get_node_logger(__file__)


class GroupCore:
    def __init__(self, name: str, **kwargs):
        self._name = name
        self._nodes = kwargs.get("nodes") or list()
        self._node_type = 'groupCore'
        self._annotation = str()
        self._note = str()

    def __repr__(self):
        return f'GroupCore({self._name})'

    def __str__(self):
        return f'GroupCore({self._name})'

    def __iter__(self):
        yield 'name', self._name
        yield 'nodes', [node.as_dict() for node in self._nodes]
        yield 'note', self._note
        yield 'annotation', self._annotation

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        logger.debug(f'Renaming group "{self._name}" to "{name}"')
        self._name = name

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, note: str):
        self._note = note

    @property
    def annotation(self):
        return self._annotation

    @annotation.setter
    def annotation(self, annotation: str):
        self._annotation = annotation

    @property
    def nodes(self):
        return self._nodes

    @property
    def node_type(self):
        return self._node_type

    def _dict(self):
        return {
            'name': self._name,
            'nodes': [node.as_dict() for node in self._nodes],
            'note': self._note,
            'annotation': self._annotation
        }

    def as_dict(self):
        return self._dict()

    def add_node(self, node_object):
        for node in self._nodes:
            if node.name == node_object.name:
                logger.error(
                    f'Failed to add Node to Group, Node "{node_object.name}" is already a member of "{self._name}" '
                    f'group.'
                )
                return
        self._nodes.append(node_object)
        # TODO
