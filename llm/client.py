from abc import ABC, abstractmethod


class LLMClient(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a text response from the LLM.
        """
        pass

    @abstractmethod
    def generate_structured(self, prompt: str, response_model):
        """
        Generate a structured response from the LLM.
        """
        pass