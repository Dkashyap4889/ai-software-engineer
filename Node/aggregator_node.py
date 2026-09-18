from .node import Node


class AggregatorNode(Node):
    def __init__(self, name, expected_branches=2):
        super().__init__(name)

        self.is_join = True
        self.expected_branches = expected_branches

    def execute(self, state):
        branches = state.get("branches", [])

        print(
            f"  Received {len(branches)} branch results"
        )

        state["aggregated"] = True
        state["branch_count"] = len(branches)

        return state