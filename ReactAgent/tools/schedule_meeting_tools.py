import json
import os
from datetime import datetime, timedelta

from lecture1.ReactAgent.llm_scheduler import LLMScheduler
from lecture1.ReactAgent.tools import mail_reply_tools


def schedule_meetings(emails: list[dict]):
    path = ensure_calendar_output_copy()
    calendar = load_calendar(path)
    path_meeting_replies = f"outputs/meetings/meeting_replies_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jsonl"


    llm_scheduler = LLMScheduler()
    for email in emails:
        success = False
        attempts = 0
        feedback_msg = None
        meeting = {}

        while not success and attempts < 3:
            # získat naplánovaný meeting
            if attempts ==0:
                suggestion = llm_scheduler.suggest_meeting(calendar=calendar, email=email)
            else:
                suggestion = llm_scheduler.suggest_meeting_feedback(calendar=calendar, email=email, feedback=feedback_msg)

            if isinstance(suggestion, str):
                try:
                    meeting = json.loads(suggestion)
                except json.JSONDecodeError:
                    feedback_msg = "Předešlý návrh nebyl validní JSON, zkus to prosím znovu."
                    attempts += 1
                    continue
            elif isinstance(suggestion, dict):
                meeting = suggestion
            else:
                feedback_msg = "Návrh má neplatný formát."
                attempts += 1
                continue

            # ověřit, že LZE mít meeting
            if is_time_available(calendar, meeting["date"], meeting["start_time"], meeting["end_time"]):
                success = True
                if attempts == 0:
                    calendar.append(meeting)
                    feedback_msg = "Schůzka byla úspěšně naplánována."
                else:
                    feedback_msg = (
                        f"Termín {email['date']} od {email['start_time']} "
                        f"do {email['end_time']} není dostupný. "
                        f"Proto navrhuji nový termín k potvrzení. Navržený termín {meeting['date']} od {meeting['start_time']} "
                        f"do {meeting['end_time']}."
                    )
            else:
                feedback_msg = (
                    f"Navržený termín {meeting['date']} od {meeting['start_time']} "
                    f"do {meeting['end_time']} není dostupný. Zkus jiný."
                )
                attempts += 1

        reply = llm_scheduler.schedule_meeting(
            message={"success": success, "attempts": attempts, "feedback": feedback_msg},
            meeting=meeting,
            email=email
        )

        mail_reply_tools.send_response(email=email, response=json.dumps(reply, ensure_ascii=False), path=path_meeting_replies)

        # uložení aktuálního kalendáře
        with open(path, "w", encoding="utf-8") as f:
            json.dump(calendar, f, ensure_ascii=False)

def load_calendar(calendar_path: str) -> list[dict]:
    """Loads calendar data from given path."""
    with open(calendar_path, encoding='utf-8') as f:
        return json.load(f)

def ensure_calendar_output_copy() -> str:
    """Copy calendar data to prevent overwriting resource data."""
    src = "input/calendar.json"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dst_dir = "outputs/meetings"
    dst = f"{dst_dir}/calendar_{timestamp}.json"

    os.makedirs(dst_dir, exist_ok=True)

    with open(src, encoding='utf-8') as f_src:
        data = f_src.read()

    with open(dst, "w", encoding='utf-8') as f_dst:
        f_dst.write(data)

    return dst

def is_time_available(existing_meetings, date: str, start_time: str, end_time: str) -> bool:
    """Checks if requested meeting time is available."""
    requested_start = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
    requested_end = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

    # mimo pracovní dobu
    if requested_start.hour < 8 or requested_end.hour > 17:
        return False

    # víkend
    if datetime.strptime(date, "%Y-%m-%d").weekday() >= 5:
        return False

    # dnešní den
    if datetime.strptime(date, "%Y-%m-%d").date() == datetime.today().date():
        return False

    for meeting in existing_meetings:
        if meeting["date"] != date:
            continue
        existing_start = datetime.strptime(f"{date} {meeting['start_time']}", "%Y-%m-%d %H:%M")
        existing_end = datetime.strptime(f"{date} {meeting['end_time']}", "%Y-%m-%d %H:%M")

        if requested_start < existing_end and requested_end > existing_start:
            return False

    return True



