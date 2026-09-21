import os

from google import genai
from google.genai import types

from .client import LLMClient


class GeminiClient(LLMClient):

    def __init__(self, model="gemini-3.5-flash-lite"):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is not set"
            )

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text

    def generate_structured(self, prompt: str, response_model):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_model,
            ),
        )

        if response.parsed is None:
            raise RuntimeError(
                "Gemini returned no structured response"
            )

        return response.parsed