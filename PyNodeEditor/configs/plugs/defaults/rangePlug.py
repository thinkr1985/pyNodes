from PyNodeEditor.core.plugCore import InputPlug
from PyNodeEditor.core.registry import RegisterInputPlug


@RegisterInputPlug
class RangePlug(InputPlug):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def main():
    return RangePlug
