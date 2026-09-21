from .node import Node

class AggregatorNode(Node):

    def __init__(self, name):
        super().__init__(name)

        self.is_join = True

        # Number of logically activated branches.
        #
        # This is dynamic because Router may select:
        #
        # ["code"]
        #
        # or:
        #
        # ["code", "research"]
        #
        self.expected_branches = (
            lambda state: len(
                state.get("routes", [])
            )
        )

    def execute(self, state):

        branches = state.get("branches", [])

        print(
            f"  Aggregator: received "
            f"{len(branches)} branches"
        )

        state["aggregated"] = True
        state["branch_count"] = len(branches)

        return state