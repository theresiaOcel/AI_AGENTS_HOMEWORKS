from ModelType import ModelType
from dotenv import load_dotenv
import os
from data.prompts import EMAIL_CLASSIFIER_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ModelType import ModelType
import json

# načtení .env
load_dotenv()

FAQ_FILE_PATH = "lecture7/data/faq.json"

class EmailClassifier:
    def __init__(self, model: ModelType = ModelType.GPT_41_mini):
        self.llm = ChatOpenAI(model=model.value, api_key=os.getenv("PROGRAMIA_OPENAI_API_KEY"))
        self.prompt = f"{EMAIL_CLASSIFIER_PROMPT}"

    def classify(self, email: str) -> str:
     
        prompt = ChatPromptTemplate(
            [
                ("system", self.prompt),
                ("system", "FAQ database:\n{faq}"),
                ("user", "Email to classify: {email}")
            ]
        )

        try:
            with open(FAQ_FILE_PATH, "r", encoding="utf-8") as f:
                faq_data = json.load(f)
        except Exception as e:
            print(f"Error reading FAQ file: {e}")
            return "unknown"

        chain = prompt | self.llm
        result = chain.invoke({
            "email": email,
            "faq": json.dumps(faq_data, ensure_ascii=False, indent=2)
        })
        category = result.content.strip().lower()

        allowed_categories = {"spam", "meeting", "auto-reply", "important", "unknown"}
        return category if category in allowed_categories else "unknown"