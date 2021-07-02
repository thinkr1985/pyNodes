"""This module initializes the core for the PyNodes"""
import os
import platform
from pathlib import Path

from nodeLogger import get_node_logger

logger = get_node_logger(__file__)

APP_NAME = "PyNodeEditor"

APP_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "configs"
)

GLOBAL_CONFIG_PATH = os.getenv("PYNODE_CONFIG_PATH")

PLATFORM = platform.system()

USER_CONFIG_PATH = None

if PLATFORM == "Windows":
    USER_CONFIG_PATH = os.path.join(
        os.path.expanduser('~/Documents'), APP_NAME
    )
elif PLATFORM == "Linux":
    USER_CONFIG_PATH = os.path.join(str(Path.home()), APP_NAME)

if not os.path.exists(USER_CONFIG_PATH):
    os.makedirs(USER_CONFIG_PATH)


class Engine(object):
    """Creating Engine class"""
    def __init__(self, **kwargs):
        """
        Initializing Engine class.
        Args:
            **kwargs: keyword arguments of this class.
        """
        self._nodes = dict()
        self._plugs = dict()
        self._init_engine()

    def __iter__(self):
        """Declaring iterator of this class"""
        yield 'nodes', self._nodes
        yield 'plugs', self._plugs

    def __getattr__(self, item):
        """Declaring get method of this class."""
        if item == "nodes":
            return self._nodes
        elif item == "plugs":
            return self._plugs

    def _dict(self):
        """
        This method casts this class into dictionary.
        Returns:
            dict: returns dictionary containing engine data.
        """
        return {
            'nodes': self._nodes,
            'plugs': self._plugs
        }

    def as_dict(self):
        """
        This method casts this class into dictionary.
        Returns:
            dict: returns dictionary containing engine data.
        """
        return self._dict()

    @property
    def nodes(self):
        """
        This property returns all nodes registered with this engine.
        Returns:
            dict: dictionary containing data of all registered nodes.
        """
        return self._nodes

    @property
    def plugs(self):
        """
        This property returns all the plugs registered in the engine.
        Returns:
            dict: returns dictionary containing all plugs data.
        """
        return self._plugs

    def get_objects(self, object_type: str):
        """
        This method gets all the objects with given type from the engine.
        Args:
            object_type (str): object type.

        Returns:
            dict: returns dictionary containing data for given object type.
        """
        if object_type == "nodes":
            return self._nodes
        elif object_type == "plugs":
            return self._plugs

    def _init_engine(self):
        """
        This method initializes the engine and registered all the nodes and
        plugs present in the default, user, global defined directories.
        Returns:
            None: Returns None.
        """
        logger.info(f'Initializing PyNode Engine..')
        py_nodes = self._get_all_py_nodes()
        self._nodes = py_nodes.get("nodes")
        self._plugs = py_nodes.get("plugs")

    def reload_engine(self):
        """
        This method reloads all the registered nodes to engine.
        Returns:
            None: Returns None.
        """
        logger.info('Reloading PyNode Engine..')
        self._init_engine()

    def _get_all_py_nodes(self):
        """
        This method gets all nodes from default, user and global directories.
        Returns:
            dict: returns the dictionary all the nodes, plugs data.
        """
        default_nodes = self._get_default_nodes()
        user_nodes = self._get_user_nodes()
        global_nodes = self._get_global_nodes()

        default_plugs = self._get_default_plugs()
        user_plugs = self._get_user_plugs()
        global_plugs = self._get_global_plugs()

        nodes = {
                'default': default_nodes,
                'user': user_nodes,
                'global': global_nodes
        }
        plugs = {
            'default': default_plugs,
            'user': user_plugs,
            'global': global_plugs
        }
        return {'nodes': nodes, 'plugs': plugs}

    @staticmethod
    def _get_py_nodes(config_path: str, node_type="nodes"):
        """
        This method gets all the nodes from given config path.
        Args:
            config_path (str): config directory path.
            node_type (str): type of nodes to found.

        Returns:
            dict: dictionary containing found node data.
        """
        if not config_path or not node_type:
            return

        nodes_dir = os.path.join(config_path, node_type)
        if not os.path.exists(nodes_dir):
            return
        py_nodes_dict = {}

        for category in os.listdir(nodes_dir):
            if category == "__pycache__":
                continue
            cat_dir = os.path.join(nodes_dir, category)
            if not os.path.isdir(cat_dir):
                continue

            py_nodes_dict.update({category: {}})

            for node_file in os.listdir(cat_dir):
                file_path = os.path.join(nodes_dir, category, node_file)
                node_name = node_file.split(".")[0]
                if node_file == "__init__.py":
                    continue
                if node_file.endswith(".py"):
                    py_nodes_dict[category].update({node_name: file_path})
        return py_nodes_dict

    def _get_default_nodes(self):
        """
        This method gets all nodes from the default config directory.
        Returns:
            dict: dictionary containing nodes data.
        """
        logger.info('Configuring all default nodes')
        return self._get_py_nodes(APP_CONFIG_PATH, node_type="nodes")

    def _get_default_plugs(self):
        """
        This method gets all plugs from the default config directory.
        Returns:
            dict: dictionary containing plugs data.
        """
        logger.info('Configuring all default plugs')
        return self._get_py_nodes(APP_CONFIG_PATH, node_type="plugs")

    def _get_user_nodes(self):
        """
        This method gets all nodes from the user config directory.
        Returns:
            dict: dictionary containing nodes data.
        """
        logger.info('Configuring all user nodes')
        return self._get_py_nodes(USER_CONFIG_PATH, node_type="nodes")

    def _get_user_plugs(self):
        """
        This method gets all plugs from the user config directory.
        Returns:
            dict: dictionary containing plugs data.
        """
        logger.info('Configuring all user plugs')
        return self._get_py_nodes(USER_CONFIG_PATH, node_type="plugs")

    def _get_global_nodes(self):
        """
        This method gets all nodes from the global config directory.
        Returns:
            dict: dictionary containing nodes data.
        """
        logger.info('Configuring all global nodes')
        return self._get_py_nodes(GLOBAL_CONFIG_PATH, node_type="nodes")

    def _get_global_plugs(self):
        """
        This method gets all nodes from the global config directory.
        Returns:
            dict: dictionary containing plug data.
        """
        logger.info('Configuring all global plugs')
        return self._get_py_nodes(GLOBAL_CONFIG_PATH, node_type="plugs")
