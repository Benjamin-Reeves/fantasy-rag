from anthropic import Anthropic

from services.config import settings


class LlmService:
    anthropic_api_key: str
    llm: Anthropic

    def __init__(self):
        self.anthropic_api_key = settings.anthropic_api_key
        self.llm = Anthropic(api_key=self.anthropic_api_key)

    def complete_message(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.2) -> str:
        try:
            response = self.llm.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"Error generating completion: {e}")
            return ""
