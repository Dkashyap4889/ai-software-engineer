from .node import Node


class TestNode(Node):
    def execute(self, state):
        attempts = state.get("attempts", 0)

        state["valid"] = attempts >= 2

        return state