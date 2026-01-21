from anthropic import Anthropic
from pydantic import BaseModel

from core.config import settings


class LlmService(BaseModel):
    anthropic_api_key: str
    llm: Anthropic

    def __init__(self, **data):
        super().__init__(**data)
        self.anthropic_api_key = settings.anthropic_api_key
        self.llm = Anthropic(api_key=self.anthropic_api_key)

    def complete_message(self, prompt: str) -> str:
        try:
            response = self.llm.completions.create(
                model="claude-haiku-4-5-20251001",
                prompt=prompt,
                max_tokens_to_sample=1000,
                temperature=0.6,
            )
            return response.completion.strip()
        except Exception as e:
            print(f"Error generating completion: {e}")
            return ""