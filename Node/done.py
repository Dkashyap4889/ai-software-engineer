from .node import Node

class DoneNode(Node):

    def execute(self, state):

        print(
            "  Done: workflow completed successfully"
        )

        return state