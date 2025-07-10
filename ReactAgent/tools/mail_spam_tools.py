import json
from datetime import datetime


def move_mails_to_trash(emails: list[dict]):
    """Simulation of moving an email to the trash"""
    path = f"outputs/spam/spam_mails_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jsonl"

    with open(path, "a", encoding="utf-8") as file:
        for email in emails:
            log_entry = {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "email": email,
            }
            json.dump(log_entry, file, ensure_ascii=False)
            file.write("\n")