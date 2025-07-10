import json
import os

from openai import OpenAI

from lecture1 import roles
from lecture1.ModelType import ModelType


class LLMEmailResponder:
    def __init__(self, model: ModelType = ModelType.GPT_41_mini):
        self.client = OpenAI(api_key=os.getenv("PROGRAMIA_OPENAI_API_KEY"))
        self.model = model

    def generate_response(self, email: dict, faq_data: list[dict]) -> str:
        """Getting an automated response to an email from LLM based on a knowledge base."""

        system_prompt = (roles.EMAIL_RESPONDER + f"\n\nZnalostní databáze:\n{json.dumps(faq_data)}")
        user_prompt = f"""
        Zpráva, na kterou chci, abys vygeneroval odpověď:
        Subject: {email.get("subject")}
        Body:  {email.get("body")}
        From:{email.get("from")}"""

        response = self.client.chat.completions.create(
            model=self.model.value,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content.strip()

