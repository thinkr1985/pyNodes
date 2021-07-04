"""Creating a simple Pass node"""
from PyNodeEditor.core.nodeCore import Node
from PyNodeEditor.core.registry import RegisterNode
from PyNodeEditor.configs.plugs.defaults.floatPlug import FloatPlug


@RegisterNode
class PassNode(Node):
    """Creating a Pass Node class"""
    def __init__(self, **kwargs):
        """
        Initializing PassNode.
        This node does not compute anything but just passes whatever is
        connected to its input to out plug.
        Args:
            **kwargs: keyword arguments of this class.
        """
        super().__init__(**kwargs)
        self.cached = False

    def setup_plugs(self):
        FloatPlug(node=self, name="Input", value=float())

    def compute(self):
        return self.inuput.value


def main():
    return PassNode
