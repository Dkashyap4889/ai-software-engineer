from .node import Node


class ErrorHandlerNode(Node):
    def execute(self, state):
        print("  ErrorHandler: handling failure")

        state["error_handled"] = True

        return state