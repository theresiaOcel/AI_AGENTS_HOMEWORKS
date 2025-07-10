import json

from lecture1.ReactAgent.llm_classifier import LLMClassifier


def load_emails(path: str) -> list:
    """Load emails from path"""
    emails = []
    with open(path, encoding="utf-8") as file:
        emails = json.load(file)
    return emails

def classify_emails(emails: list[dict]) -> dict:
    """Classify all emails using LLMClassifier"""

    llm_classifier = LLMClassifier()
    categorized = {
        "spam": [],
        "meetings": [],
        "auto-reply": [],
        "important": [],
        "unknown": [],
    }

    for email in emails:
        category = llm_classifier.classify_email(email)
        categorized[category].append(email)

    return categorized


