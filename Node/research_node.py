import time

from .node import Node


class ResearchNode(Node):
    def execute(self, state):
        print("  Research: starting")

        time.sleep(2)

        print("  Research: finished")

        state["research"] = "completed"

        return state