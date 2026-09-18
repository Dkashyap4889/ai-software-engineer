import time

from .node import Node


class ImplementNode(Node):
    def execute(self, state):
        attempts = state.get("implement_attempts", 0) + 1
        state["implement_attempts"] = attempts

        print(
            f"  Implement: attempt {attempts}"
        )

        time.sleep(2)

        if attempts == 1:
            raise RuntimeError(
                "Implementation failed"
            )

        print("  Implement: finished")

        state["code"] = "generated"

        return state