from .node import Node

class TestNode(Node):

    def __init__(self, name, command_runner):
        super().__init__(name)
        self.command_runner = command_runner

    def execute(self, state):

        strategy = state.get("implementation_strategy")
        test_plan = state.get("test_plan")

        if not strategy:
            raise RuntimeError("No implementation strategy found")

        if not test_plan:
            raise RuntimeError("No test implementation plan found")

        technologies = [
            t.lower()
            for t in strategy.technologies
        ]

        print(" Test: running generated automated tests...")

        if "pytest" in technologies:
            result = self.command_runner.run(
                ["pytest"],
                cwd="generated_app"
            )

        elif "jest" in technologies:
            result = self.command_runner.run(
                ["npm", "test", "--", "--runInBand"],
                cwd="generated_app"
            )

        else:
            raise RuntimeError(
                "No test runner configured for technologies: "
                + ", ".join(strategy.technologies)
            )

        state["test_result"] = result
        state["valid"] = result["success"]

        if not result["success"]:
            print(" Tests failed")
            print(result["stdout"])
            print(result["stderr"])
        else:
            print(" All automated tests passed")

        return state