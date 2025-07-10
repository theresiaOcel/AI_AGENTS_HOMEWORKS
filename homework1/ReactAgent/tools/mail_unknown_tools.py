import json
from datetime import datetime


def mark_unknown_email(emails: list[dict]):
    """Simulation of marking emails as unknown"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"outputs/unknown/unknown_mails_{timestamp}.jsonl"

    with open(path, "a", encoding="utf-8") as file:
        if not emails:
            log_entry = {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "email": "Žádný email nebyl označen jako 'unknown'."
            }
            json.dump(log_entry, file, ensure_ascii=False)
            file.write("\n")
        else:
            for email in emails:
                log_entry = {
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "email": email
                }
                json.dump(log_entry, file, ensure_ascii=False)
                file.write("\n")