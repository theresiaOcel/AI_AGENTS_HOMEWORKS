import json
from datetime import datetime

from lecture1.ReactAgent.llm_email_responder import LLMEmailResponder


def reply_to_emails(emails: list[dict]):
    """Reply to all emails that generate an automatic response based on the knowledge base"""

    with open("input/faq_knowledge.json", encoding="utf-8") as f:
        faq_data = json.load(f)

    # pro "odeslání" emailu
    # realně: zápis odpovědí do souboru
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"outputs/replies/replies_{timestamp}.jsonl"

    # pro každý email se vygeneruje email, který se má odeslat
    llm_responder = LLMEmailResponder()

    for email in emails:
        reply = llm_responder.generate_response(email=email, faq_data=faq_data)
        send_response(email=email, response=reply, path=path)

def send_response(email: dict, response: str, path:str):
    """Simulating sending a reply to an email. Saving email and reply to a file."""

    if isinstance(response, str):
        try:
            response = json.loads(response)
        except json.decoder.JSONDecodeError:
            pass

    log_entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "email": email,
        "response": response,
    }

    with open(path, "a", encoding="utf-8") as file:
        json.dump(log_entry, file, ensure_ascii=False)
        file.write("\n")
