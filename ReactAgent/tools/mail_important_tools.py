import json
from datetime import datetime


def marks_mails_as_important(emails: list[dict]):
    """Simulation of marking an email as important"""
    path = f"outputs/important/important_mails_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jsonl"

    with open(path, "a", encoding="utf-8") as file:
        for email in emails:
            log_entry = {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "email": email,
            }
            json.dump(log_entry, file, ensure_ascii=False)
            file.write("\n")