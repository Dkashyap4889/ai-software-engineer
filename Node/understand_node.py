from .node import Node
from Model.model import RequirementAnalysis

class UnderstandNode(Node):

    def execute(self, state):

        requirement = state.get("requirement")

        if not requirement:
            raise RuntimeError(
                "No requirement found in state"
            )

        print(
            "  Understand: asking Gemini to analyze requirement..."
        )

        analysis = self.llm.generate_structured(
            f"""
        You are an AI Software Engineer responsible for understanding
        software requirements.

        Requirement:

        {requirement}

        Determine:

        1. Application type.
        2. Main features.
        3. Technologies/frameworks appropriate for implementation.
        4. Whether implementation/code is required.
        5. Whether additional research is required.

        IMPORTANT:

        For any requirement that asks to build, create, implement,
        develop, or modify software, set needs_code to true.

        Set needs_research to true only when external information
        is genuinely required before implementation.

        Return ONLY the structured requirement analysis.
        """,
            RequirementAnalysis
        )

        print(
            "  Understand: structured analysis received"
        )

        state["understanding"] = analysis

        return state