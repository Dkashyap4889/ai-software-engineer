from .node import Node
from Model.model import TestImplementationPlan

class TestImplementNode(Node):

    def __init__(self, name, llm, file_writer):
        super().__init__(name, llm)
        self.file_writer = file_writer

    def execute(self, state):

        requirement = state.get("requirement")
        understanding = state.get("understanding")
        strategy = state.get("implementation_strategy")
        implementation_plan = state.get("implementation_plan")

        if not requirement:
            raise RuntimeError(
                "No requirement found for test implementation"
            )

        if not understanding:
            raise RuntimeError(
                "No requirement analysis found"
            )

        if not strategy:
            raise RuntimeError(
                "No implementation strategy found"
            )

        if not implementation_plan:
            raise RuntimeError(
                "No implementation plan found"
            )

        print(
            "  TestImplement: asking Gemini to generate automated tests..."
        )

        test_plan = self.llm.generate_structured(
            f"""
You are an AI Software Engineer responsible for
implementing automated tests.

Requirement:
{requirement}

Requirement analysis:
{understanding.model_dump()}

Implementation strategy:
{strategy.model_dump()}

Application implementation:
{implementation_plan.model_dump()}

Generate automated tests that verify the actual
requirements of the application.

Rules:

1. Use the technologies and testing approach
   appropriate for the application.

2. Generate complete executable test files.

3. Tests must verify actual application behavior,
   not merely that files exist.

4. Cover the important requirements and features.

5. Do not generate placeholder tests.

6. Do not explain the tests.

7. Return only the structured test implementation plan.

For every test file provide:
- relative file path
- complete file contents
""",
            TestImplementationPlan
        )

        print(
            f"  TestImplement: Gemini generated "
            f"{len(test_plan.tests)} test files"
        )

        written_tests = self.file_writer.write_files(
            test_plan.tests
        )

        print(
            f"  TestImplement: wrote "
            f"{len(written_tests)} test files"
        )

        state["test_plan"] = test_plan
        state["test_artifacts"] = written_tests

        return state