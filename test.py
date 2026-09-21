from pydantic import BaseModel
from llm import GeminiClient


class RequirementAnalysis(BaseModel):
    application_type: str
    features: list[str]
    technologies: list[str]
    needs_code: bool
    needs_research: bool


def main():

    llm = GeminiClient()

    analysis = llm.generate_structured(
        """
        Analyze this software requirement:

        Build a React application with two numeric inputs
        and an Add button that displays the sum.

        Determine what application it is, its features,
        technologies, whether code needs to be written,
        and whether additional research is required.
        """,
        RequirementAnalysis
    )

    print("\n========== STRUCTURED RESPONSE ==========")
    print(analysis)
    print("=========================================")

    print("\nCode required:", analysis.needs_code)
    print("Research required:", analysis.needs_research)


if __name__ == "__main__":
    main()