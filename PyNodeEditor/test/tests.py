"""Module to write unittest for PyNodeCore"""
import unittest
from PyNodeEditor.core import engine
from PyNodeEditor.core.nodeLogger import get_node_logger

logger = get_node_logger(__file__)


class TestNodes(unittest.TestCase):

    def test_create_node(self):
        node = engine.create_node(name="MyTestNode")
        node.rename("MyRenamedNode")
        node.note = "My Test Node"
        node.annotation = "My Text Annotation"

        logger.info(f'output plug : {node.output_plug.name}')
        logger.info(f'output plug type : {node.output_plug.node_type}')
        logger.info(node.output_plug.name)

        engine.create_plug(node=node, name="MyInputPlug", value=4)
        logger.info(node.as_dict())
        node2 = engine.create_node("MyTestNode")
        logger.info(engine.get_nodes())

    def test_create_group(self):
        group = engine.create_group(name="MyTestGroup")
        group.rename("MyRenamedNode")
        group.note = "My Test Node"
        group.annotation = "My Text Annotation"


if __name__ == "__main__":
    unittest.main()

