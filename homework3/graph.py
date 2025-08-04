from ModelType import ModelType
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


# načtení .env
load_dotenv()


class MailAgent:
    def __init__(self, ModelType: ModelType, tools: list, prompt: str):
        self.llm = ChatOpenAI(api_key=os.getenv("PROGRAMIA_OPENAI_API_KEY"), model=ModelType.GPT_41_mini.value)
        self.tools = tools
        self.prompt = prompt
    

    def create_agent(self):
        self.graph = create_react_agent(
            model = self.llm,
            tools = self.tools,
            prompt = self.prompt
        )