import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from lecture1 import roles
from lecture1.ModelType import ModelType

load_dotenv()

class LLMScheduler:
    def __init__(self, model: ModelType = ModelType.GPT_41_mini):
        self.client = OpenAI(api_key=os.getenv("PROGRAMIA_OPENAI_API_KEY"))
        self.model = model

    def suggest_meeting(self, calendar,email: dict) -> dict:
        sys_prompt = f"{roles.MEETING_SUGGEST}\n\nKALENDÁŘ:\n{json.dumps(calendar, ensure_ascii=False)}"
        user_prompt = f"""
                Zpráva, obsahující žádost o schůzku:
                Subject: {email.get("subject")}
                Body:  {email.get("body")}
                From:{email.get("from")}"""

        response = self.client.chat.completions.create(
            model=self.model.value,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        content = response.choices[0].message.content.strip()

        print(f"...NAVRHNUTÝ MEETING...\n{content}")

        try:
            proposed_meeting = json.loads(content)
            return proposed_meeting
        except json.JSONDecodeError:
            print("Chyba při parsování odpovědi LLM:", content)
            return {}

    def suggest_meeting_feedback(self, calendar: list[dict], email: dict, feedback: str) -> dict:
        sys_prompt = f"{roles.MEETING_SUGGEST}\n\nKALENDÁŘ:\n{json.dumps(calendar, ensure_ascii=False)}"
        user_prompt = f"""Zpráva, obsahující žádost o schůzku:
            Subject: {email.get("subject")}
            Body:  {email.get("body")}
            From: {email.get("from")}
        
            POZNÁMKA: Předchozí návrh schůzky nebyl možný: {feedback}
            Zkus prosím jiný návrh.
            """

        response = self.client.chat.completions.create(
            model=self.model.value,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )

        content = response.choices[0].message.content.strip()
        print(f"...NAVRHNUTÝ MEETING když neprošel na poprvé...\n{content}")

        try:
            proposed_meeting = json.loads(content)
            return proposed_meeting
        except json.JSONDecodeError:
            print("Chyba při parsování odpovědi LLM:", content)
            return {}

    def schedule_meeting(self, message:dict, meeting:dict, email:dict) -> dict:
        sys_prompt = (f"{roles.MEETING_REPLY}\n\nZpráva o stavu:\n{json.dumps(message, ensure_ascii=False)}"
                      f"\n\nNavržený meeting:\n{json.dumps(meeting, ensure_ascii=False)}")
        user_prompt =  f"""
                Zpráva, obsahující žádost o schůzku:
                Subject: {email.get("subject")}
                Body:  {email.get("body")}
                From:{email.get("from")}"""

        response = self.client.chat.completions.create(
            model=self.model.value,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        content = response.choices[0].message.content.strip()

        try:
            proposed_meeting = json.loads(content)
            return proposed_meeting
        except json.JSONDecodeError:
            print("Chyba při parsování odpovědi LLM:", content)
            return {}
