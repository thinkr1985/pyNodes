"""Utility functions"""
import os
import json
from xml.etree import cElementTree
from collections import defaultdict

from nodeLogger import get_node_logger

logger = get_node_logger(__file__)


def read_file(file_path: str = None):
    if os.path.exists(file_path):
        with open(file_path, 'r') as rp:
            return rp.readlines()
    else:
        logger.error(f'Failed to read file {file_path}')
        raise FileExistsError(f'File {file_path} does not exists!')


def read_json(json_path: str = None):
    """This function reads the given json file.
    Args:
        json_path (str): json file path in string format.

    Returns:
        dict: Returns json data in dictionary format.
    """
    if os.path.exists(json_path):
        with open(json_path, "r") as fp:
            data_dict = json.load(fp)
            return data_dict
    else:
        logger.error(f'Failed to read file {json_path}')
        raise FileExistsError(f'File {json_path} does not exists!')


def write_json(path: str, data: dict):
    """This function writes provided dictionary object into json format.
    Args:
        path (str): Full file path where you want to write json.
        data (dictionary): Dictionary object which you want to write.

    Returns:
        (None): Returns None.
    """
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f'Json written at {path}')


def etree_to_dict(xml_tree):
    """This function converts the xml tree object into dictionary.
    Args:
        xml_tree (cElementTree.XML): XML Tree object.

    Returns:
        (dictionary): Returns dictionary object.
    """
    final_dict = {xml_tree.tag: {} if xml_tree.attrib else None}
    children = list(xml_tree)

    if children:
        default_dict = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                default_dict[k].append(v)
        final_dict = {
            xml_tree.tag:
                {
                    k: v[0] if len(v) == 1 else v for k, v in default_dict.
                    items()
                }
        }

    if xml_tree.attrib:
        final_dict[
            xml_tree.tag].update((k, v) for k, v in xml_tree.attrib.items())

    if xml_tree.text:
        text = xml_tree.text.strip()
        if children or xml_tree.attrib:
            if text:
                final_dict[xml_tree.tag]['#text'] = text
        else:
            final_dict[xml_tree.tag] = text
    return final_dict


def convert_xml_to_dict(xml_path: str):
    """This function converts given XML to dictionary.
    Args:
        xml_path (str): Full path of XML file.

    Returns:
        (dictionary): Returns the dictionary converted from given XML file.
    """

    logger.info(f'Reading XML : {xml_path}')
    read_ = read_file(xml_path)
    dict_ = etree_to_dict(cElementTree.XML(str(read_)))
    return dict_
