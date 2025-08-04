from ModelType import ModelType
from tools.email_tools import EmailTools
from tools.calendar_tools import CalendarTools
from graph import MailAgent
from data.prompts import AI_AGENT_PROMPT
import json
import time

EMAILS_PATH = "lecture7/data/emails.json"

def load_emails(filepath: str) -> list[dict]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            emails = json.load(f)
        return emails
    except Exception as e:
        print(f"[ERROR] Unable to load emails: {e}")
        return []

if __name__ == "__main__":
    print("[INFO] Starting AI Agent for email processing...")
    time.sleep(1)

    emails = load_emails(EMAILS_PATH)
    if not emails:
        print("[ERROR] No emails found to process.")
        exit()

    emailtools = EmailTools()
    calendartools = CalendarTools()


    agent = MailAgent(
        ModelType= ModelType.GPT_41_mini,
        tools=emailtools.get_tools() + calendartools.get_tools(),
        prompt=AI_AGENT_PROMPT)
    agent.create_agent()


    for idx, email in enumerate(emails, start=1):
        print(f"[INFO] Processing email {idx + 1}/{len(emails)}: {email.get('subject', 'No Subject')}")
        user_message = f"Nový email:\n{email}"
        
        events = agent.graph.stream({"messages": [("user", user_message)]}, stream_mode="values")
        for event in events:
            last_message = event["messages"][-1]
            last_message.pretty_print()
    
    print("[INFO] All emails processed successfully.")
   

