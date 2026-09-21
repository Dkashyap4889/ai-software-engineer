from .node import Node

class FailedNode(Node):

    def execute(self, state):

        print(
            "  Failed: workflow could not complete"
        )

        state["workflow_failed"] = True

        return state