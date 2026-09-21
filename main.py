from edge import Edge
from graph import Graph
from executor import GraphExecutor
from Node import (
    AggregatorNode,
    ErrorHandlerNode,
    ImplementNode,
    DoneNode,
    FailedNode,
    PlanNode,
    ImplementationRepairNode,
    ResearchNode,
    RouterNode,
    TestNode,
    TestImplementNode,
    UnderstandNode,
    StartNode,
    EnvironmentNode,
    TestRepairNode
)
from llm.gemini_client import GeminiClient
from tools.command_runner import CommandRunner
from tools.file_writer import FileWriter

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

def test_failed(state):
    return not state.get("valid", False)

# ============================================================
# CREATE DEPENDENCIES
# ============================================================

llm = GeminiClient()

file_writer = FileWriter(
    "generated_app"
)

command_runner = CommandRunner()

# ============================================================
# CREATE NODES
# ============================================================
start = StartNode(
    "Start"
)

understand = UnderstandNode(
    "Understand",
    llm=llm
)

plan = PlanNode(
    "Plan",
    llm=llm
)

router = RouterNode(
    "Router"
)

implement = ImplementNode(
    "Implement",
    llm=llm,
    file_writer=file_writer
)

research = ResearchNode(
    "Research"
)

aggregator = AggregatorNode(
    "Aggregator"
)

test = TestNode(
    "Test",
    command_runner=command_runner
)

test_implement_node = TestImplementNode(
    "TestImplement",
    llm=llm,
    file_writer=file_writer
)

environment = environment = EnvironmentNode(
    "Environment",
    command_runner
)

error_handler = ErrorHandlerNode(
    "ErrorHandler"
)

implementation_repair = ImplementationRepairNode(
    "ImplementationRepair"
)

test_repair = TestRepairNode(
    "TestRepair",
    llm,
    file_writer
)

done = DoneNode(
    "Done"
)

failed = FailedNode(
    "Failed"
)

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
graph.add_edge(Edge(test_implement_node, environment))
graph.add_edge(Edge(environment, test))
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

graph.add_edge(
    Edge(aggregator, test_implement_node)
)

graph.add_edge(Edge(test_implement_node, environment))
graph.add_edge(Edge(environment, test))

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
        error_handler,
        implementation_repair
    )
)

graph.add_edge(
    Edge(
        implementation_repair,
        implement
    )
)

graph.add_edge(
    Edge(test, done, is_valid)
)

graph.add_edge(
    Edge(test, failed, test_failed)
)

graph.add_edge(
    Edge(test,
        done,
        condition=lambda state, error: (
            error is None
            and state.get("test_result", {}).get("success") is True
        ))
)

graph.add_edge(
    Edge(test,
        test_repair,
        condition=lambda state, error: (
            error is None
            and state.get("test_result", {}).get("success") is False
        ))
)

graph.add_edge(Edge(test_repair, test))

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