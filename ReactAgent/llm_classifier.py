
import os
from openai import OpenAI
from dotenv import load_dotenv
from unicodedata import category

from lecture1 import roles
from lecture1.ModelType import ModelType

load_dotenv()

class LLMClassifier:
    def __init__(self, model: ModelType = ModelType.GPT_41_mini):
        self.client = OpenAI(api_key=os.getenv("PROGRAMIA_OPENAI_API_KEY"))
        self.model = model

    def classify_email(self, email:dict) -> str:
        """Uses LLM to classify an email into one of the predefined categories.
        Returns one of following categories: spam, meetings, auto-reply, important, unknown"""

        user_prompt = f"""Email:
        Subject: {email.get("subject")}
        Body: {email.get("body")}"""

        response = self.client.chat.completions.create(
            model = self.model.value,
            messages=[
                {"role": "system", "content": roles.EMAIL_CLASSIFIER},
                {"role": "user", "content": user_prompt},
            ]
        )

        cat = response.choices[0].message.content.strip().lower() # category
        allowed = {"spam", "meetings", "auto-reply", "important", "unknown"}
        return cat if cat in allowed else "unknown"
