"""Creating a simple addition node"""
from PyNodeEditor.core.nodeCore import Node
from PyNodeEditor.core.registry import RegisterNode
from PyNodeEditor.configs.plugs.defaults.floatPlug import FloatPlug


@RegisterNode
class MultiplyNode(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cached = False

    def setup_plugs(self):
        FloatPlug(node=self, name="Number1", value=float())
        FloatPlug(node=self, name="Number2", value=float())

    def compute(self):
        input_1_value = self.Number1.value or 0.0
        input_2_value = self.Number2.value or 0.0

        return float(input_1_value) * float(input_2_value)


def main():
    return MultiplyNode
