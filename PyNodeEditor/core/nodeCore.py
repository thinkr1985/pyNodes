"""Module to create Node class"""
import traceback

from nodeLogger import get_node_logger
from plugCore import OutputPlug
from registry import NameCheck

logger = get_node_logger(__file__)


class Node(object):
    """Creating Node class"""
    def __init__(self, **kwargs):
        """
        Initializing Node class.
        Args:
            name (str): Name of the Node.
            **kwargs : Extra parameters to pass this class.
        """
        self._name = kwargs.get("name")
        self._input_plugs = list()
        self._output_plug = OutputPlug(node=self, name="Out", value=None)
        self._icon = kwargs.get("icon") or str()
        self._annotation = kwargs.get("annotation") or str()
        self._note = kwargs.get("node") or str()
        self._cached = False
        self._is_dirty = False
        self._node_type = 'node'

        self.setup_plugs()

    def __repr__(self):
        """Representing this class"""
        return f'Node({self._name}, {self._annotation}, {self._note})'

    def __str__(self):
        """Representing this class in string format"""
        return f'Node({self._name}, {self._annotation}, {self._note})'

    def __iter__(self):
        """
        Creating iterator for this class.
        Returns (dict): Returns dict.

        """
        yield 'name', self._name
        yield 'plugs', [x.as_dict() for x in self._input_plugs]
        yield 'icon', self._icon,
        yield 'annotation', self._annotation
        yield 'note', self._note
        yield 'cached', self._cached
        yield 'isDirty', self._is_dirty
        yield 'isAnimated', self.is_animated

    def __getattr__(self, plug_name: str):
        """
        setting getattr method to get input plugs
        Args:
            plug_name (str): Name of the plug.

        Returns:
            InputPlug: Returns the Input Plug object.
        """
        found = False
        for item in self._input_plugs:
            if item.name == plug_name:
                return item

        if not found:
            logger.error(f'Plug not exists with name "{plug_name}" in the node "{self._name}"')
            raise NameError

    def _dict(self):
        """
        This method casts this node into dictionary.
        Returns:
            dict: Returns casted dictionary.
        """
        return{
            'name': self._name,
            'plugs': [x.as_dict() for x in self._input_plugs],
            'icon': self._icon,
            'annotation': self._annotation,
            'note': self._note,
            'cached': self._cached,
            'isDirty': self._is_dirty,
            'isAnimated': self.is_animated,
        }

    def as_dict(self):
        """
        This property returns node data in dictionary format.
        Returns:
            dict: returns dictionary containing node data.
        """
        return self._dict()

    @property
    def node_type(self):
        """
        This property returns node type of node.
        Returns:
            str: Returns node type of this class.
        """
        return self._node_type

    @property
    def name(self):
        """
        This property gets the name of the node.
        Returns:
            str: Returns name of the node.
        """
        return self._name

    @NameCheck
    def rename(self, name: str):
        """
        This method sets the name of node.
        Args:
            name (str): Name to be given.

        Returns:
            None: Returns None.
        """
        logger.debug(f'Renaming node "{self._name}" to "{name}"')
        self._name = str(name)

    def parents(self):
        """
        Gets the parent nodes.
        Returns:
            list: Returns list containing parent nodes.
        """
        logger.debug(f'Getting all the parents of the node "{self._name}"')
        parents = []
        for plug in self._input_plugs:
            if plug.connection:
                if plug.connection.source_node not in parents:
                    parents.append(plug.connection.source_node)
        return parents

    def children(self):
        """
        gets all children of the nodes.
        Returns:
            list: Returns list containing child nodes.
        """
        logger.debug(f'Getting all the children nodes of node "{self._name}"')
        children = []
        if self._output_plug.connections:
            for con in self._output_plug.connections:
                dest_node = con.destination_node
                if dest_node not in children:
                    children.append(dest_node)
        else:
            logger.debug(f'No children found in the node"{self._name}"')
        return children

    @property
    def input_plugs(self):
        """
        This property gets all the input plugs of this node.
        Returns:
            list: Returns list of all input plug of this node.
        """
        return self._input_plugs

    @property
    def output_plug(self):
        """
        This property gets the output plug of this node.
        Returns:
            returns Output plug object.
        """
        return self._output_plug

    @property
    def output(self):
        """
        This property gets the computed value of the output plug.
        Returns:
            returns the computed value of the node.
        """
        return self._output_plug.value

    @property
    def is_dirty(self):
        """
        This property checks if node is dirty.
        Returns:
            bool: Returns True if its dirty else returns False.
        """
        return self._is_dirty

    @is_dirty.setter
    def is_dirty(self, value: bool):
        """
        This method sets the node's dirty status.
        Args:
            value (bool): True / False.

        Returns:
            None: Returns None.
        """
        if isinstance(value, bool):
            self._is_dirty = value

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

    @property
    def annotation(self):
        """
        This method gets the annotation of the node.
        Returns:
            str: Returns node's annotation.
        """
        return self._annotation

    @annotation.setter
    def annotation(self, annotation_text: str):
        """
        This method sets the annotations of the node.
        Args:
            annotation_text (str): Annotation string to add.

        Returns:
            None: Returns None.
        """
        self._annotation = str(annotation_text)
        logger.info(f'Annotation for node "{self._name}" set to {annotation_text}')

    @property
    def note(self):
        """
        This property gets the note of the node.
        Returns:
            str: Returns note of this node.
        """
        return self._note

    @note.setter
    def note(self, note: str):
        """
        This method sets the note to the node.
        Args:
            note (str): Note to set on this node.

        Returns:
            None: Returns None.
        """
        self._note = str(note)
        logger.info(f'note for node "{self._name}" set to {note}')

    @property
    def cached(self):
        """
        This property gets the cached state of the node.
        Returns:
            bool: Returns True if the node's cached mode on ON.
        """
        return self._cached

    @cached.setter
    def cached(self, value: bool):
        """
        This method set the cached state of the node.
        Args:
            value (bool): Value to set for cached attribute of the node.

        Returns:
            None: Returns None.
        """
        if isinstance(value, bool):
            self._cached = value
            logger.info(f'Cache state set for node "{self._name}" to {value}')

    @property
    def is_animated(self):
        """
        This property checks if any of the input plugs are animated.
        Returns:
            bool: Returns True if its animated else returns False
        """
        for plug in self._input_plugs:
            if plug.is_animated:
                return True

    def get_child(self, child_node_name):
        """
        This method gets the child node with matching name.
        Args:
            child_node_name (str): Name of the child to find.

        Returns:
            (Node): Returns the Node object.
        """
        logger.debug(f'Getting child with name "{child_node_name}" from the node "{self._name}"')
        found = False
        for child in self.children():
            if child.name == child_node_name:
                return child
        if not found:
            logger.error(f'Failed to find child with name "{child_node_name}" in the node "{self._name}"')
            raise NameError

    def get_plug(self, plug_name: str):
        """
        This method gets the plug with matching name.
        Args:
            plug_name (str): name of the plug.

        Returns:
            InputPlug: returns the matching plug object.
        """
        logger.debug(f'Getting plug with name "{plug_name}" from the node "{self._name}"')
        for plug_ in self._input_plugs:
            if plug_.name == plug_name:
                return plug_

    def add_plug(self, plug):
        """
        This method adds the given plug to the node.
        Args:
            plug (InputPlug): Input Plug object.

        Returns:
            None: Returns None.
        """
        self._input_plugs.append(plug)

    def setup_plugs(self):
        """This method supposed to override while creating your own node."""
        pass

    def compute(self):
        """
        This method computes the result of all inputs.
        Returns:

        """
        pass

    def evaluate(self):
        """
        This method calls compute method to evaluate the node.
        Returns:
            Returns the result of computation.
        """
        logger.debug(f'Evaluating Node "{self.name}" in cached state:{self._cached}')

        try:
            if self.cached:
                if self._output_plug.value:
                    return self._output_plug.value
                else:
                    self._output_plug.value = self.compute()
                    self.is_dirty = False
                    return self._output_plug.value
            else:
                self._output_plug.value = self.compute()

                self.is_dirty = False
                return self._output_plug.value
        except Exception as err:
            logger.error(f'Failed to compute node "{self.name}": {err}')
            logger.error(msg=traceback.format_exc())
            self._is_dirty = True

    def evaluate_children(self):
        """
        This method evaluates all its children
        Returns:
            None: Returns None.
        """
        logger.debug(f'Triggering evaluation of children of node "{self._name}"')
        for child in self.children():
            child.evaluate()
