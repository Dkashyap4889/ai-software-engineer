from .node import Node

class ImplementationRepairNode(Node):

    def execute(self, state):

        attempts = (
            state.get(
                "implementation_repair_attempts",
                0
            ) + 1
        )

        state["implementation_repair_attempts"] = attempts

        print(
            f"  ImplementationRepair: attempt {attempts}"
        )

        if attempts > 3:
            raise RuntimeError(
                "Maximum implementation repair attempts exceeded"
            )

        # Temporary repair behavior.
        #
        # Later this node will receive the actual error,
        # ask the LLM to diagnose it, modify the implementation
        # and send it back through Implement/Test.

        return state
