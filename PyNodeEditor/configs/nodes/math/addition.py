"""Creating a simple addition node"""
from PyNodeEditor.core.nodeCore import Node
from PyNodeEditor.core.registry import RegisterNode
from PyNodeEditor.configs.plugs.defaults.floatPlug import FloatPlug


@RegisterNode
class AdditionNode(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setup_plugs(self):
        FloatPlug(node=self, name="Number 1", value=1.0)
        FloatPlug(node=self, name="Number 2", value=1.0)

    def compute(self):
        input_1_value = self.get_plug("Number 1").value
        input_2_value = self.get_plug("Number 2").value

        return input_1_value + input_2_value


def main():
    return AdditionNode
