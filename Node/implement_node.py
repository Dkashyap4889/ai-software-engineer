from .node import Node
from Model.model import ImplementationPlan
from tools.file_writer import FileWriter

class ImplementNode(Node):

    def __init__(self, name, llm, file_writer):
        super().__init__(name, llm)

        self.file_writer = file_writer

    def execute(self, state):

        requirement = state.get("requirement")
        understanding = state.get("understanding")
        strategy = state.get("implementation_strategy")

        if not requirement:
            raise RuntimeError(
                "No requirement found for implementation"
            )

        if not understanding:
            raise RuntimeError(
                "No requirement analysis found"
            )

        if not strategy:
            raise RuntimeError(
                "No implementation strategy found"
            )

        print(
            "  Implement: asking Gemini to generate implementation..."
        )

        plan = self.llm.generate_structured(
            f"""
You are an AI Software Engineer responsible for implementing
software requirements.

Implement the following requirement:

{requirement}

Requirement analysis:
{understanding.model_dump()}

Implementation strategy:
{strategy.model_dump()}

Generate the complete project required to implement the
requirement.

For every required file provide:

- relative file path
- complete file contents

Requirements:

- Produce a runnable application.
- Follow the implementation strategy.
- Use the technologies selected during planning.
- Keep the implementation minimal and maintainable.
- Do not include unnecessary files or dependencies.
- Do not explain the code.
- Return only the implementation plan according to the schema.
""",
            ImplementationPlan
        )

        print(
            f"  Implement: Gemini generated "
            f"{len(plan.files)} files"
        )

        written_files = self.file_writer.write_files(
            plan.files
        )

        print(
            f"  Implement: wrote "
            f"{len(written_files)} files to disk"
        )

        state["implementation_plan"] = plan
        state["artifacts"] = written_files

        return state