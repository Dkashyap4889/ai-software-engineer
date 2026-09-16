import time

from edge import Edge
from graph import Graph
from executor import GraphExecutor


class Node:
    def __init__(self, name):
        self.name = name

    def execute(self, state):
        return state


class RouterNode(Node):
    def execute(self, state):
        state["routes"] = ["code", "research"]
        return state

class RepairNode(Node):
    def execute(self, state):
        print("  Repair: fixing implementation")

        state["attempts"] = (
            state.get("attempts", 0) + 1
        )

        state["code"] = "repaired"

        return state

class TestNode(Node):
    def execute(self, state):
        attempts = state.get("attempts", 0)

        state["valid"] = attempts >= 2

        return state

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

class ResearchNode(Node):
    def execute(self, state):
        print("  Research: starting")

        time.sleep(2)

        print("  Research: finished")

        state["research"] = "completed"

        return state

class ErrorHandlerNode(Node):
    def execute(self, state):
        print("  ErrorHandler: handling failure")

        state["error_handled"] = True

        return state

def is_code(state):
    return state["route"] == "code"


def is_research(state):
    return state["route"] == "research"

def is_valid(state):
    return state.get("valid", False)


def needs_repair(state):
    return not state.get("valid", False)


def max_attempts_reached(state):
    return state.get("attempts", 0) >= 3

def needs_code(state):
    return "code" in state.get("routes", [])


def needs_research(state):
    return "research" in state.get("routes", [])

def has_error(state, error):
    return error is not None

# Nodes
start = Node("Start")
understand = Node("Understand")
plan = Node("Plan")
router = RouterNode("Router")
implementation_repair = RepairNode(
    "ImplementationRepair"
)
test_repair = RepairNode(
    "TestRepair"
)
implement = ImplementNode("Implement")
research = ResearchNode("Research")
aggregator = AggregatorNode("Aggregator")
test = TestNode("Test")
done = Node("Done")
failed = Node("Failed")
error_handler = ErrorHandlerNode("ErrorHandler")

# Graph
graph = Graph()

for node in [
    start,
    understand,
    plan,
    router,
    implement,
    research,
    test,
    implementation_repair,
    test_repair,
    failed,
    aggregator,
    done,
    error_handler
]:
    graph.add_node(node)


graph.add_edge(Edge(start, understand))
graph.add_edge(Edge(understand, plan))
graph.add_edge(Edge(plan, router))

graph.add_edge(
    Edge(
        router,
        implement,
        condition=needs_code
    )
)

graph.add_edge(
    Edge(
        router,
        research,
        condition=needs_research
    )
)

graph.add_edge(
    Edge(
        implement,
        aggregator,
        condition=lambda state, error: error is None
    )
)

graph.add_edge(
    Edge(
        implement,
        error_handler,
        condition=has_error
    )
)
graph.add_edge(Edge(research, aggregator))

graph.add_edge(Edge(aggregator, test))

graph.add_edge(
    Edge(
        test,
        done,
        condition=is_valid
    )
)

graph.add_edge(
    Edge(
        test,
        failed,
        condition=max_attempts_reached
    )
)

graph.add_edge(
    Edge(
        test,
        test_repair,
        condition=needs_repair
    )
)

graph.add_edge(
    Edge(
        test_repair,
        test
    )
)

graph.add_edge(
    Edge(
        error_handler,
        implementation_repair
    )
)

graph.add_edge(
    Edge(
        implementation_repair,
        aggregator
    )
)

# Display graph
graph.display()


# Execute graph
executor = GraphExecutor(graph)

final_state = executor.run(start)


print("\nFinal state:")
print(final_state)
print("\nExecution Events:")
print("-" * 80)

for event in executor.events:
    print(event)