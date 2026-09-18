from .node import Node


class RepairNode(Node):
    def execute(self, state):
        print("  Repair: fixing implementation")

        state["attempts"] = (
            state.get("attempts", 0) + 1
        )

        state["code"] = "repaired"

        return state