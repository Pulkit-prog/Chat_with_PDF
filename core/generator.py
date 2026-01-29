"""
Groq LLM response generator.
"""

from groq import Groq
from config import Config


class GroqGenerator:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant answering strictly based on the provided document context. "
                            "If information is missing, answer conservatively."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=Config.LLM_TEMPERATURE,
                max_tokens=Config.LLM_MAX_TOKENS,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"LLM generation failed: {str(e)}"
