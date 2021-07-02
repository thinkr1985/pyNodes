"""Creating Group class"""
from nodeLogger import get_node_logger
from registry import NameCheck, RegisterNode
logger = get_node_logger(__file__)


@RegisterNode
class Group(object):
    """Creating a Group class"""
    def __init__(self, **kwargs):
        """
        Initializing Group class.
        Args:
            **kwargs: keyword arguments of this class.
        """
        self._name = kwargs.get("name")
        self._nodes = kwargs.get("nodes") or list()
        self._node_type = 'group'
        self._annotation = str()
        self._note = str()

    def __repr__(self):
        """Representing this class"""
        return f'Group({self._name})'

    def __str__(self):
        """String presentation of this class"""
        return f'Group({self._name})'

    def __iter__(self):
        """Defining iterator for this class"""
        yield 'name', self._name
        yield 'nodes', [node.as_dict() for node in self._nodes]
        yield 'note', self._note
        yield 'annotation', self._annotation

    @property
    def name(self):
        """
        This property gets the name of the group.
        Returns:
            str: returns the name of the group.
        """
        return self._name

    @NameCheck
    def rename(self, name: str):
        """
        This method renames the group
        Args:
            name (str): Name string to rename.

        Returns:
            None: Returns None.
        """
        logger.debug(f'Renaming group "{self._name}" to "{name}"')
        self._name = name

    @property
    def note(self):
        """
        This property gets the note of the group.
        Returns:
            str: Returns the note of the group in string format.
        """
        return self._note

    @note.setter
    def note(self, note: str):
        """
        This setter function sets the note on the group.
        Args:
            note (str): Note to set on the group.

        Returns:
            None: Returns None.
        """
        self._note = str(note)

    @property
    def annotation(self):
        """
        This property gets the annotation of the group.
        Returns:
            str: Returns the annotation of the group in string format.
        """
        return self._annotation

    @annotation.setter
    def annotation(self, annotation: str):
        """
        This setter function sets the annotation on the group.
        Args:
            annotation (str): Annotation to set.

        Returns:
            None: Returns None.
        """
        self._annotation = str(annotation)

    @property
    def nodes(self):
        """
        This property gets all nodes exists inside this group.
        Returns:
            list: Returns list containing all nodes exists within this group.
        """
        return self._nodes

    @property
    def node_type(self):
        """
        This property gets node type of this group.
        Returns:
            str: returns node type in string format.
        """
        return self._node_type

    def _dict(self):
        """
        This method casts this node to dictionary format.
        Returns:
            dict: returns dictionary representation of this class.
        """
        return {
            'name': self._name,
            'nodes': [node.as_dict() for node in self._nodes],
            'note': self._note,
            'annotation': self._annotation
        }

    def as_dict(self):
        """
        This method returns dictionary presentation of this class.
        Returns:
            dict: returns dictionary.
        """
        return self._dict()

    def add_node(self, node_object):
        """
        This method adds the given node to the class.
        Args:
            node_object (Node): Node object to add inside this group.

        Returns:
            None: Returns None.
        """
        for node in self._nodes:
            if node.name == node_object.name:
                logger.error(
                    f'Failed to add Node to Group, Node "{node_object.name}" '
                    f'is already a member of "{self._name}" group.'
                )
                return
        self._nodes.append(node_object)
        # TODO
