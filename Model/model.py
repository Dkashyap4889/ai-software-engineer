from pydantic import BaseModel
from llm import GeminiClient


class RequirementAnalysis(BaseModel):
    application_type: str
    features: list[str]
    technologies: list[str]
    needs_code: bool
    needs_research: bool

class GeneratedFile(BaseModel):
    path: str
    content: str


class ImplementationPlan(BaseModel):
    files: list[GeneratedFile]

class RepairPlan(BaseModel):
    diagnosis: str
    files: list[GeneratedFile]


class TestStep(BaseModel):
    action: str
    target: str | None = None
    value: str | None = None


class TestCase(BaseModel):
    name: str
    description: str
    type: str
    expected: str
    steps: list[TestStep] = []

class GeneratedTest(BaseModel):
    path: str
    content: str


class TestImplementationPlan(BaseModel):
    tests: list[GeneratedTest]

class EnvironmentStrategy(BaseModel):
    language: str
    package_manager: str
    dependency_file: str
    install_command: list[str]
    test_command: list[str]

class ImplementationStrategy(BaseModel):
    approach: str
    technologies: list[str]
    architecture: str
    steps: list[str]
    test_cases: list[TestCase]
    environment_strategy: EnvironmentStrategy

class RepairPlan(BaseModel):
    diagnosis: str
    changes: list[GeneratedFile]