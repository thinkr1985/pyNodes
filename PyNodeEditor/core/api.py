"""Functions to interact with engine and network"""
import traceback
import importlib.util

import constants
import utils
from nodeLogger import get_node_logger
from connectionCore import Connection
from nodeCore import Node

logger = get_node_logger(__file__)


def get_object_types_from_engine(object_type="nodes"):
    """
    This function gets all nodes with given type from the engine.
    Args:
        object_type (str): type of node.

    Returns:
        list: Returns list containing all node types in string format.
    """
    if object_type not in ("nodes", "plugs"):
        logger.error(
            f'Undefined object type "{object_type}",'
            f' valid object types are "nodes", "plugs"!'
        )
        raise TypeError

    object_types = []
    objects = constants.ENGINE.get_objects(object_type)
    for category, subcategory in objects.items():
        if subcategory:
            for category_name, objects in subcategory.items():
                object_types.extend(objects)
    return object_types


def get_engine_node_types():
    """
    This function gets all node types from engine.
    Returns:
        list: Returns list of available node types.
    """
    return get_object_types_from_engine(object_type="nodes")


def get_engine_plug_types():
    """
    This function gets all plug types from engine.
    Returns:
        list: Returns list containing available plug types.
    """
    return get_object_types_from_engine(object_type="plugs")


def create_node(name: str, node_type: str):
    """
    This function creates the node with given name and type.
    Args:
        name (str): Name of the node to create.
        node_type (str): type of node to create.

    Returns:
        Node: Returns the Node object.
    """
    if not name or not node_type:
        logger.error('Node Must have name/node-type!')
        raise NameError('Name/Node Type not provided to create a node!')

    engine_node_types = get_engine_node_types()
    if node_type not in engine_node_types:
        logger.error(
            f'Failed to create node, node-type "{node_type}" '
            f'is not registered with the engine.'
        )
        raise TypeError(
            f'Node-type "{node_type}" is not registered with the engine.'
        )

    logger.info(f'Creating "{node_type}" node with name "{name}"')

    for category, subcategory in constants.ENGINE.nodes.items():
        if subcategory:
            for category_name, objects in subcategory.items():
                if node_type in objects:
                    node_file = objects.get(node_type)
                    try:
                        module_source = importlib.util.spec_from_file_location(
                            "module.name", node_file)
                        module = importlib.util.module_from_spec(module_source)
                        module_source.loader.exec_module(module)
                        object_ = module.main()
                        return object_(name=name)
                    except Exception as err:
                        logger.error(
                            f'Failed to create Node {name} with error : {err}'
                        )
                        logger.error(traceback.format_exc())
                        return


def get_all_nodes_from_network():
    """
    This function gets all the node present in the network.
    Returns:
        dict: Returns dict containing node data.
    """
    return constants.NETWORK.nodes


def connect_nodes(source_plug, destination_plug):
    """
    This function creates connection in between given plugs
    Args:
        source_plug: OutputPlug of the source node.
        destination_plug: input node of the destination plug.

    Returns:
        Connection: returns the connection object.
    """
    if not source_plug or not destination_plug:
        logger.error(
            'Failed to connect nodes, source/destination plugs not provided.'
        )
        raise NotImplemented(
            'Failed to connect nodes, source/destination plugs not provided.'
        )

    connection = Connection(
        source_plug=source_plug,
        destination_plug=destination_plug
    )
    return connection


def save_network(file_path):
    """
    This function saves the current network in the given file path.
    Args:
        file_path (str): Full path of the file to save network.

    Returns:
        bool: Returns True on successful write else returns False.
    """
    network_dict = constants.NETWORK.as_dict()
    try:
        utils.write_json(file_path, network_dict)
        return True
    except Exception as err:
        logger.error(f'Failed to save network : {err}')
        logger.error(traceback.format_exc())


def load_network_from_file(filepath):
    pass
