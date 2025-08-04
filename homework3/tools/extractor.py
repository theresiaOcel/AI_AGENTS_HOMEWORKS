from ModelType import ModelType
from dotenv import load_dotenv
import os
from data.prompts import EMAIL_EXTRACTOR_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ModelType import ModelType
import json

# načtení .env
load_dotenv()

class EmailExtractor:
    def __init__(self, model: ModelType = ModelType.GPT_41_mini):
        self.llm = ChatOpenAI(model=model.value, api_key=os.getenv("PROGRAMIA_OPENAI_API_KEY"))
        self.prompt = f"{EMAIL_EXTRACTOR_PROMPT}"

    def extract(self, email: str) -> dict:
        prompt = ChatPromptTemplate(
            [
                ("system", self.prompt),
                ("user", f"Email: {email}")
            ]
        )

        chain = prompt | self.llm
        result = chain.invoke({"Email": email})

        print(f"[TOOL Extractor] Extracted details: {result.content}")
        
        try:
            details = json.loads(result.content)
        except json.JSONDecodeError:
            details = {"date": "unknown", "time": "unknown", "participants": ["unknown"]}

        return details