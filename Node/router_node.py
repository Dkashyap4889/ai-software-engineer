from .node import Node


class RouterNode(Node):
    def execute(self, state):
        state["routes"] = ["code", "research"]
        return state