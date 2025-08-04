from ModelType import ModelType
from dotenv import load_dotenv
import os
from data.prompts import EMAIL_AUTO_REPLY_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ModelType import ModelType
import json

# načtení .env
load_dotenv()

FAQ_FILE_PATH = "lecture7/data/faq.json"

class EmailReplier:
    def __init__(self, model: ModelType = ModelType.GPT_41_mini):
        self.llm = ChatOpenAI(model=model.value, api_key=os.getenv("PROGRAMIA_OPENAI_API_KEY"))
        self.prompt = f"{EMAIL_AUTO_REPLY_PROMPT}"

    def auto_reply(self, email: dict) -> str:
     
        prompt = ChatPromptTemplate(
            [
                ("system", self.prompt),
                ("system", "FAQ database:\n{faq}"),
                ("user", "EMAIL:\n{email}")
            ]
        )

        try:
            with open(FAQ_FILE_PATH, "r", encoding="utf-8") as f:
                faq_data = json.load(f)
        except Exception as e:
            print(f"Error reading FAQ file: {e}")
            return "__NO_REPLY__"
        
        email_text = f"Předmět: {email['subject']}\nOd: {email['from']}\nTělo:\n{email['body']}"

        chain = prompt | self.llm

        result = chain.invoke({
            "email": email_text,
            "faq": json.dumps(faq_data, ensure_ascii=False, indent=2)
        })
        response = result.content.strip()

        return response if response and "__NO_REPLY__" not in response else "__NO_REPLY__"