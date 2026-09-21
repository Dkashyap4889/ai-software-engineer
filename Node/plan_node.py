from .node import Node
from Model.model import ImplementationStrategy

class PlanNode(Node):

    def execute(self, state):

        requirement = state.get("requirement")
        understanding = state.get("understanding")

        if not requirement:
            raise RuntimeError(
                "No requirement found for planning"
            )

        if not understanding:
            raise RuntimeError(
                "No requirement analysis found for planning"
            )

        print(
            "  Plan: asking Gemini to create implementation strategy..."
        )

        strategy = self.llm.generate_structured(
            f"""
        You are an AI Software Engineer.

        Create an implementation strategy for this requirement.

        Requirement:
        {requirement}

        Requirement analysis:
        {understanding.model_dump()}

        Determine:

        1. Technical approach
        2. Technologies
        3. Architecture
        4. Implementation steps
        5. Validation test cases

        The validation test cases must verify that the
        implemented software actually satisfies the requirement.

        For every test case provide:

        - description
        - type
        - expected result

        Test types may include:

        - structural
        - build
        - behavioral

        Do NOT generate source code.
        Do NOT generate files.
        Do NOT return file paths.

        Return ONLY the implementation strategy.
        """,
            ImplementationStrategy
        )

        print(
            "  Plan: implementation strategy received"
        )

        state["implementation_strategy"] = strategy

        return state