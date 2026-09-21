from .node import Node


class EnvironmentNode(Node):

    def __init__(self, name, command_runner):
        super().__init__(name)
        self.command_runner = command_runner

    def execute(self, state):

        strategy = state.get("implementation_strategy")

        if not strategy:
            raise RuntimeError(
                "No implementation strategy found"
            )

        environment = strategy.environment_strategy

        if not environment:
            raise RuntimeError(
                "No environment strategy found"
            )

        print(" Environment: installing dependencies...")

        result = self.command_runner.run(
            environment.install_command,
            cwd="generated_app"
        )

        state["environment_result"] = result

        if not result["success"]:
            raise RuntimeError(
                "Dependency installation failed:\n"
                + result["stderr"]
            )

        print(" Environment: dependencies installed")

        return state