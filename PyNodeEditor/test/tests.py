"""Module to write unittest for PyNodeCore"""
import unittest
import pep8

from PyNodeEditor.core import api
from PyNodeEditor.core import utils
from PyNodeEditor.core.nodeLogger import get_node_logger

logger = get_node_logger(__file__)


class TestNodes(unittest.TestCase):

    def test_pep8_syntax(self):
        """Test that we conform to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        module_files = utils.get_all_module_files(file_ext=".py")
        result = pep8style.check_files(module_files)
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_addition_node(self):
        add_node = api.create_node(
            name="MyTestNode", node_type="addition"
        )
        another_node = api.create_node(
            name="MyExtraNode", node_type="addition"
        )

        add_node.Number1.value = 5
        self.assertEqual(5, add_node.Number1.value)
        add_node.Number2.value = 6
        self.assertEqual(6, add_node.Number2.value)
        self.assertEqual(11, add_node.output)

        another_node.Number1.value = 3
        self.assertEqual(3, another_node.Number1.value)
        another_node.Number2.value = 3
        self.assertEqual(3, another_node.Number2.value)
        self.assertEqual(6, another_node.output)

        api.connect_nodes(add_node.output_plug, another_node.Number1)
        api.connect_nodes(add_node.output_plug, another_node.Number2)

        '''
         ____            _____
        5|   |--(11)--> 3|    | 
        6|   |--(11)--> 3|    |-----> |22|
         -----           _____
         add_node   +   another_node
        '''

        self.assertEqual(11, another_node.Number2.value)
        self.assertEqual(22, another_node.output)

        add_node.Number1.value = 10

        '''
          ____              _____
        10|   |--(16)--> 16|    | 
        6 |   |--(16)--> 16|    |-----> |32|
          -----            _____
         add_node   +   another_node
        '''
        self.assertEqual(16, another_node.Number1.value)
        self.assertEqual(32, another_node.output)

        api.disconnect_plug(another_node.Number1)
        add_node.Number1.value = 45

        self.assertEqual(16, another_node.Number1.value)
        self.assertEqual(51, another_node.Number2.value)
        self.assertEqual(67, another_node.output)

    def test_subtract_node(self):
        add_node = api.create_node(
            name="MyTestNode2", node_type="subtraction"
        )
        another_node = api.create_node(
            name="MyExtraNode2", node_type="subtraction"
        )

        add_node.Number1.value = 5
        self.assertEqual(5, add_node.Number1.value)
        add_node.Number2.value = 3
        self.assertEqual(3, add_node.Number2.value)
        self.assertEqual(2, add_node.output)

        another_node.Number1.value = 3
        self.assertEqual(3, another_node.Number1.value)
        another_node.Number2.value = 3
        self.assertEqual(3, another_node.Number2.value)
        self.assertEqual(0, another_node.output)

        api.connect_nodes(add_node.output_plug, another_node.Number1)
        api.connect_nodes(add_node.output_plug, another_node.Number2)

        self.assertEqual(2, another_node.Number1.value)
        self.assertEqual(2, another_node.Number2.value)
        self.assertEqual(0, another_node.output)

        api.disconnect_plug(another_node.Number2)
        add_node.Number1.value = 50

        self.assertEqual(47, another_node.Number1.value)
        self.assertEqual(2, another_node.Number2.value)
        self.assertEqual(45, another_node.output)

    def test_group_node(self):
        add_node = api.create_node(
            name="MyTestNode2", node_type="subtraction"
        )
        another_node = api.create_node(
            name="MyExtraNode2", node_type="subtraction"
        )
        add_node.Number1.value = 5
        add_node.Number2.value = 7
        group = api.create_group(name="MyTestGroup",
                                 nodes=[add_node, another_node]
                                 )


if __name__ == "__main__":
    unittest.main()
