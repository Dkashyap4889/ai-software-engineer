from .node import Node

class RouterNode(Node):

    def execute(self, state):

        understanding = state.get("understanding")

        if not understanding:
            raise RuntimeError(
                "No requirement analysis found for routing"
            )

        routes = []

        if understanding.needs_code:
            routes.append("code")

        if understanding.needs_research:
            routes.append("research")

        if not routes:
            raise RuntimeError(
                "No execution route selected"
            )

        state["routes"] = routes

        print(
            f"  Router: selected routes {routes}"
        )

        return state