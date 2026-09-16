import time
from pathlib import Path

from edge import Edge
from graph import Graph
from executor import GraphExecutor


# ============================================================
# Base Node
# ============================================================

class Node:
    def __init__(self, name):
        self.name = name

    def execute(self, state):
        return state


# ============================================================
# Start
# ============================================================

class StartNode(Node):
    def execute(self, state):
        print("  Starting AI Software Engineer workflow")
        time.sleep(0.5)

        state["requirement"] = (
            "Build a React app with two numeric inputs "
            "and an Add button that displays the sum."
        )

        return state


# ============================================================
# Understand
# ============================================================

class UnderstandNode(Node):
    def execute(self, state):
        print("  Understanding requirement...")
        time.sleep(1)

        state["understood"] = True

        return state


# ============================================================
# Plan
# ============================================================

class PlanNode(Node):
    def execute(self, state):
        print("  Planning implementation...")
        time.sleep(1)

        state["plan"] = [
            "Create React application",
            "Create two number inputs",
            "Create Add button",
            "Display calculated result"
        ]

        return state


# ============================================================
# Router
# ============================================================

class RouterNode(Node):
    def execute(self, state):
        print("  Router: deciding workflow branches...")
        time.sleep(0.8)

        state["routes"] = ["code", "research"]

        return state


# ============================================================
# Research
# ============================================================

class ResearchNode(Node):
    def execute(self, state):
        print("  Research: checking React implementation approach...")
        time.sleep(1.5)

        state["research"] = "completed"

        print("  Research: finished")

        return state


# ============================================================
# Implement
# ============================================================

class ImplementNode(Node):

    def execute(self, state):

        attempt = state.get("implement_attempts", 0) + 1
        state["implement_attempts"] = attempt

        print(f"  Implement: attempt {attempt}")

        time.sleep(1)

        # ----------------------------------------------------
        # Intentionally fail the first implementation attempt.
        # This demonstrates graph-based recovery.
        # ----------------------------------------------------

        if attempt == 1:
            print("  Implement: simulated implementation failure")
            raise RuntimeError("Implementation failed")

        # ----------------------------------------------------
        # Second attempt succeeds and generates the React app.
        # ----------------------------------------------------

        print("  Implement: generating React application...")
        time.sleep(1.5)

        app_dir = Path("generated-react-app")
        src_dir = app_dir / "src"

        src_dir.mkdir(parents=True, exist_ok=True)

        # ----------------------------------------------------
        # package.json
        # ----------------------------------------------------

        (app_dir / "package.json").write_text(
            """{
  "name": "generated-react-app",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.4",
    "vite": "^6.3.5"
  }
}
""",
            encoding="utf-8"
        )

        # ----------------------------------------------------
        # vite.config.js
        # ----------------------------------------------------

        (app_dir / "vite.config.js").write_text(
            """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()]
})
""",
            encoding="utf-8"
        )

        # ----------------------------------------------------
        # index.html
        # ----------------------------------------------------

        (app_dir / "index.html").write_text(
            """<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Generated App</title>
  </head>

  <body>
    <div id="root"></div>

    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""",
            encoding="utf-8"
        )

        # ----------------------------------------------------
        # src/main.jsx
        # ----------------------------------------------------

        (src_dir / "main.jsx").write_text(
            """import React from 'react'
import ReactDOM from 'react-dom/client'

import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
""",
            encoding="utf-8"
        )

        # ----------------------------------------------------
        # src/App.jsx
        # ----------------------------------------------------

        (src_dir / "App.jsx").write_text(
            """import { useState } from 'react'

function App() {
  const [firstNumber, setFirstNumber] = useState('')
  const [secondNumber, setSecondNumber] = useState('')
  const [result, setResult] = useState(null)

  const addNumbers = () => {
    const sum = Number(firstNumber) + Number(secondNumber)

    setResult(sum)
  }

  return (
    <div className="container">

      <h1>Hello World</h1>

      <input
        type="number"
        placeholder="First number"
        value={firstNumber}
        onChange={(event) => setFirstNumber(event.target.value)}
      />

      <input
        type="number"
        placeholder="Second number"
        value={secondNumber}
        onChange={(event) => setSecondNumber(event.target.value)}
      />

      <button onClick={addNumbers}>
        Add
      </button>

      {result !== null && (
        <p>
          Result: {result}
        </p>
      )}

    </div>
  )
}

export default App
""",
            encoding="utf-8"
        )

        # ----------------------------------------------------
        # src/index.css
        # ----------------------------------------------------

        (src_dir / "index.css").write_text(
            """body {
  font-family: Arial, sans-serif;
  margin: 0;
  background: #f5f5f5;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-top: 100px;
}

input {
  padding: 10px;
  width: 200px;
  font-size: 16px;
}

button {
  padding: 10px 24px;
  font-size: 16px;
  cursor: pointer;
}

p {
  font-size: 20px;
  font-weight: bold;
}
""",
            encoding="utf-8"
        )

        print("  Implement: React application generated")

        state["code"] = "generated"

        return state


# ============================================================
# Error Handler
# ============================================================

class ErrorHandlerNode(Node):

    def execute(self, state):
        print("  ErrorHandler: handling implementation failure...")
        time.sleep(1)

        state["error_handled"] = True

        return state


# ============================================================
# Implementation Repair
# ============================================================

class RepairNode(Node):

    def execute(self, state):
        print("  ImplementationRepair: preparing retry...")
        time.sleep(1)

        state["repair_attempted"] = True

        return state


# ============================================================
# Aggregator / Join
# ============================================================

class AggregatorNode(Node):

    def __init__(self, name):
        super().__init__(name)

        # The Router creates two branches:
        #
        # 1. Implement
        # 2. Research
        #
        # Aggregator waits for both.
        self.is_join = True
        self.expected_branches = 2

    def execute(self, state):

        print("  Aggregator: combining implementation and research...")
        time.sleep(0.8)

        branches = state.get("branches", [])

        state["aggregated"] = True
        state["branch_count"] = len(branches)

        print(
            f"  Aggregator: received {len(branches)} branch results"
        )

        return state


# ============================================================
# Test
# ============================================================

class TestNode(Node):

    def execute(self, state):

        print("  Test: validating generated React application...")
        time.sleep(1)

        app_dir = Path("generated-react-app")

        required_files = [
            app_dir / "package.json",
            app_dir / "vite.config.js",
            app_dir / "index.html",
            app_dir / "src" / "main.jsx",
            app_dir / "src" / "App.jsx",
            app_dir / "src" / "index.css"
        ]

        missing_files = [
            str(file)
            for file in required_files
            if not file.exists()
        ]

        if missing_files:

            print("  Test: FAILED")
            print("  Missing files:")

            for file in missing_files:
                print(f"    - {file}")

            state["valid"] = False

            return state

        # ----------------------------------------------------
        # Validate actual application content.
        # ----------------------------------------------------

        app_content = (
            app_dir / "src" / "App.jsx"
        ).read_text(encoding="utf-8")

        checks = [
            "useState",
            "First number",
            "Second number",
            "Add",
            "Number(firstNumber)",
            "Number(secondNumber)",
            "setResult"
        ]

        missing_content = [
            check
            for check in checks
            if check not in app_content
        ]

        if missing_content:

            print("  Test: FAILED")
            print("  Missing expected implementation:")
            
            for item in missing_content:
                print(f"    - {item}")

            state["valid"] = False

            return state

        print("  Test: PASSED")
        print("  React application structure is valid")

        state["valid"] = True

        return state


# ============================================================
# Done
# ============================================================

class DoneNode(Node):

    def execute(self, state):

        print()
        print("  ========================================")
        print("  AI SOFTWARE ENGINEER COMPLETED")
        print("  ========================================")
        print()
        print("  React application generated successfully.")
        print("  Location: ./generated-react-app")
        print()

        time.sleep(0.5)

        return state


# ============================================================
# Failed
# ============================================================

class FailedNode(Node):

    def execute(self, state):

        print()
        print("  ========================================")
        print("  WORKFLOW FAILED")
        print("  ========================================")
        print()

        return state


# ============================================================
# Conditions
# ============================================================

def needs_code(state):
    return "code" in state.get("routes", [])


def needs_research(state):
    return "research" in state.get("routes", [])


def implementation_succeeded(state, error=None):
    return error is None and state.get("code") == "generated"


def implementation_failed(state, error=None):
    return error is not None


def is_valid(state):
    return state.get("valid") is True


def is_failed(state):
    return state.get("valid") is False


# ============================================================
# Build Graph
# ============================================================

def build_graph():

    graph = Graph()

    # --------------------------------------------------------
    # Nodes
    # --------------------------------------------------------

    start = StartNode("Start")
    understand = UnderstandNode("Understand")
    plan = PlanNode("Plan")
    router = RouterNode("Router")

    implement = ImplementNode("Implement")
    research = ResearchNode("Research")

    error_handler = ErrorHandlerNode("ErrorHandler")
    implementation_repair = RepairNode(
        "ImplementationRepair"
    )

    aggregator = AggregatorNode("Aggregator")

    test = TestNode("Test")

    done = DoneNode("Done")
    failed = FailedNode("Failed")

    # --------------------------------------------------------
    # Register nodes
    # --------------------------------------------------------

    nodes = [
        start,
        understand,
        plan,
        router,
        implement,
        research,
        error_handler,
        implementation_repair,
        aggregator,
        test,
        done,
        failed
    ]

    for node in nodes:
        graph.add_node(node)

    # --------------------------------------------------------
    # Main flow
    # --------------------------------------------------------

    graph.add_edge(
        Edge(start, understand)
    )

    graph.add_edge(
        Edge(understand, plan)
    )

    graph.add_edge(
        Edge(plan, router)
    )

    # --------------------------------------------------------
    # Router -> parallel branches
    # --------------------------------------------------------

    graph.add_edge(
        Edge(
            router,
            implement,
            needs_code
        )
    )

    graph.add_edge(
        Edge(
            router,
            research,
            needs_research
        )
    )

    # --------------------------------------------------------
    # Implementation success
    # --------------------------------------------------------

    graph.add_edge(
        Edge(
            implement,
            aggregator,
            implementation_succeeded
        )
    )

    # --------------------------------------------------------
    # Implementation failure
    # --------------------------------------------------------

    graph.add_edge(
        Edge(
            implement,
            error_handler,
            implementation_failed
        )
    )

    # ErrorHandler -> Repair
    graph.add_edge(
        Edge(
            error_handler,
            implementation_repair
        )
    )

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Repair goes BACK to Implement.
    #
    # This creates a graph cycle:
    #
    # Implement
    #    ↓ failure
    # ErrorHandler
    #    ↓
    # ImplementationRepair
    #    ↓
    # Implement
    #
    # The executor allows this because max_steps
    # protects against infinite execution.
    # --------------------------------------------------------

    graph.add_edge(
        Edge(
            implementation_repair,
            implement
        )
    )

    # --------------------------------------------------------
    # Research -> Aggregator
    # --------------------------------------------------------

    graph.add_edge(
        Edge(
            research,
            aggregator
        )
    )

    # --------------------------------------------------------
    # Aggregator -> Test
    # --------------------------------------------------------

    graph.add_edge(
        Edge(
            aggregator,
            test
        )
    )

    # --------------------------------------------------------
    # Test -> Done
    # --------------------------------------------------------

    graph.add_edge(
        Edge(
            test,
            done,
            is_valid
        )
    )

    # --------------------------------------------------------
    # Test -> Failed
    # --------------------------------------------------------

    graph.add_edge(
        Edge(
            test,
            failed,
            is_failed
        )
    )

    return graph, start


# ============================================================
# Main
# ============================================================

def main():

    print()
    print("========================================")
    print("     AI SOFTWARE ENGINEER POC")
    print("========================================")
    print()

    print("Requirement:")
    print(
        "Build a React app with two numbers "
        "and an Add button."
    )

    print()
    print("Building execution graph...")
    print()

    graph, start = build_graph()

    # --------------------------------------------------------
    # Display graph topology
    # --------------------------------------------------------

    graph.display()

    print("========================================")
    print("Starting Graph Execution")
    print("========================================")
    print()

    # --------------------------------------------------------
    # Create executor
    # --------------------------------------------------------

    executor = GraphExecutor(
        graph,
        max_steps=50,
        max_workers=4
    )

    # --------------------------------------------------------
    # Execute graph
    # --------------------------------------------------------

    try:

        final_state = executor.run(start)

        print()
        print("========================================")
        print("Execution Complete")
        print("========================================")

        print()
        print("Final State:")
        print(final_state)

        print()
        print("Generated application:")
        print(
            Path("generated-react-app")
            .resolve()
        )

    except Exception as exc:

        print()
        print("========================================")
        print("Execution Error")
        print("========================================")

        print(exc)


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()