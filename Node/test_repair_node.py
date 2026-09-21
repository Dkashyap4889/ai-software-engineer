from .node import Node
from Model.model import RepairPlan


class TestRepairNode(Node):

    def __init__(self, name, llm, file_writer):
        super().__init__(name, llm)
        self.file_writer = file_writer

    def execute(self, state):
        test_result = state.get("test_result")

        if not test_result:
            raise RuntimeError("No test result found")

        print(" TestRepair: analyzing test failure...")

        repair_plan = self.llm.generate_structured(
            f"""
You are an AI Software Engineer repairing an application after
automated tests failed.

Requirement:
{state.get("requirement")}

Implementation:
{state.get("implementation_plan").model_dump()}

Tests:
{state.get("test_plan").model_dump()}

Test result:
{test_result}

Analyze the failure and generate the MINIMAL changes required
to make the failing tests pass.

Rules:
1. Diagnose the actual failure.
2. Modify only files that need modification.
3. Do not rewrite the entire application.
4. Do not weaken or remove tests just to make them pass.
5. Preserve the original requirements.
6. Return complete file contents for every modified file.
7. No explanations outside the structured response.
""",
            RepairPlan
        )

        print(f" TestRepair: {repair_plan.diagnosis}")

        written_files = self.file_writer.write_files(
            repair_plan.changes
        )

        state["repair_plan"] = repair_plan
        state["repair_artifacts"] = written_files
        state["repair_attempts"] = state.get("repair_attempts", 0) + 1

        return state