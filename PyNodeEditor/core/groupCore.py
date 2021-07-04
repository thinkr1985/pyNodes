"""Creating Group class"""
from nodeLogger import get_node_logger
from registry import CheckDuplicateRegistryName, RegisterGroup
from exceptions import MissingPlugError
from constants import DEFAULT_GROUP_ICON

logger = get_node_logger(__file__)


@RegisterGroup
class Group(object):
    """Creating a Group class"""
    def __init__(self, **kwargs):
        """
        Initializing Group class.
        Args:
            **kwargs: keyword arguments of this class.
        """
        self._name = kwargs.get("name").strip()
        self._nodes = kwargs.get("nodes") or list()
        self._node_type = 'group'
        self._annotation = kwargs.get("annotation") or str()
        self._note = kwargs.get("note") or str()
        self._cached = False
        self._is_dirty = False
        self._icon = kwargs.get("icon") or DEFAULT_GROUP_ICON
        for node in self._nodes:
            node.group = self

    def __repr__(self):
        """Representing this class"""
        return f'Group({self._name}) at {hex(id(self))}'

    def __str__(self):
        """String presentation of this class"""
        return f'Group({self._name})'

    def __iter__(self):
        """Defining iterator for this class"""
        yield 'name', self._name
        yield 'nodes', [node.as_dict() for node in self._nodes]
        yield 'note', self._note
        yield 'annotation', self._annotation
        yield 'icon', self._icon
        yield 'isDirty', self._is_dirty
        yield 'cached', self._cached

    def __getattr__(self, node_name: str):
        """
        setting getattr method to get input plugs
        Args:
            node_name (str): Name of the node.

        Returns:
            InputPlug: Returns the Input Plug object.
        """
        found = False
        for item in self.nodes:
            if item.name == node_name:
                return item

        if not found:
            raise MissingPlugError(
                f'Plug not exists with name "{node_name}" '
                f'in the node "{self._name}"'
            )

    @property
    def name(self):
        """
        This property gets the name of the group.
        Returns:
            str: returns the name of the group.
        """
        return self._name

    @CheckDuplicateRegistryName
    def rename(self, name: str):
        """
        This method renames the group
        Args:
            name (str): Name string to rename.

        Returns:
            None: Returns None.
        """
        logger.debug(f'Renaming group "{self._name}" to "{name.strip()}"')
        self._name = str(name).strip()

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

    @property
    def cached(self):
        """
        This property gets the cached state of the group.
        Returns:
            bool: Returns True if the group's cached mode on ON.
        """
        return self._cached

    @cached.setter
    def cached(self, value: bool):
        """
        This method set the cached state of the group.
        Args:
            value (bool): Value to set for cached attribute of the group.

        Returns:
            None: Returns None.
        """
        if isinstance(value, bool):
            self._cached = value
            logger.info(f'Cache state set for group "{self._name}" to {value}')

    @property
    def is_dirty(self):
        """
        This property checks if group is dirty.
        Returns:
            bool: Returns True if its dirty else returns False.
        """
        return self._is_dirty

    @is_dirty.setter
    def is_dirty(self, value: bool):
        """
        This method sets the group's dirty status.
        Args:
            value (bool): True / False.

        Returns:
            None: Returns None.
        """
        if isinstance(value, bool):
            self._is_dirty = value

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
            'annotation': self._annotation,
            'icon': self._icon,
            'isDirty': self._is_dirty,
            'cached': self._cached
        }

    @property
    def icon(self):
        """
        This property gets node's the icon path.
        Returns:
            str: returns the node's icon path.
        """
        return self._icon

    @icon.setter
    def icon(self, icon_path: str):
        """
        This method sets the icon path of the node.
        Args:
            icon_path (str): Icon file's full path.

        Returns:
            None: Returns Node.
        """
        self._icon = icon_path
        logger.info(f'Icon path for node "{self._name}" set to {icon_path}')

    def as_dict(self):
        """
        This method returns dictionary presentation of this class.
        Returns:
            dict: returns dictionary.
        """
        return self._dict()

