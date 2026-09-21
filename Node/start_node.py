from .node import Node

class StartNode(Node):

    def execute(self, state):

        state["requirement"] = (
            "Build a FastAPI task management API with SQLite persistence, CRUD operations, status filtering, validation, and automated pytest tests."
        )

        print("  Start: requirement received")

        return state