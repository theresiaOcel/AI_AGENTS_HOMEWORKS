from langchain_google_community.calendar.toolkit import CalendarToolkit
from langchain_google_community.calendar.utils import (
    get_google_credentials,
    build_resource_service,
)
from langchain.tools import tool

from datetime import datetime, timedelta
import pytz

CREDENTIALS_PATH = "lecture7/credentials/google_calendar_credential.json"
TOKEN_PATH = "lecture7/credentials/tokens/google_calendar_token.json"

credentials = get_google_credentials(
    token_file=TOKEN_PATH,
    client_secrets_file=CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/calendar"])

api_resource = build_resource_service(credentials=credentials)

toolkit = CalendarToolkit(api_resource=api_resource)
tools = toolkit.get_tools()


def to_rfc3339_range(date_str: str, time_str: str, hours: int = 1):
    """Returns start_time a end_time in RFC3339 format for specified hours."""
    local_tz = pytz.timezone("Europe/Prague")
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")  # ← upraven formát
    start_dt = local_tz.localize(dt)
    end_dt = start_dt + timedelta(hours=hours)
    return start_dt.isoformat(), end_dt.isoformat()


@tool
def check_availability(date: str, time:str) -> str:
    """Check if there is a free 1-hour slot in the calendar on a given date and time.
    
    Args:
        date (str): The date to check availability for.
        time (str): The time to check availability for.
        
    Returns: 'free' or 'busy'."""
    return check_availability_raw(date, time)

    

def check_availability_raw(date: str, time:str) -> str:
    try:
        start_time, end_time = to_rfc3339_range(date, time)
        print(f"[DEBUG] Checking availability between {start_time} and {end_time}")


        events_res = api_resource.events().list( # type: ignore[attr-defined]
            calendarId='primary',
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy='startTime',
            timeZone='Europe/Prague'
        ).execute()

        print(f"[TOOL check_availability]: events: {events_res}...")

        events = events_res.get('items', [])

        return "free" if not events else "busy"
    except Exception as e:
        print(f"Error checking availability: {e}")
        return "unknown"

    

@tool
def get_next_available_slot(date: str, time: str) -> dict:
    """
    Checks whether the given date is available or suggests the nearest alternative available time.
    
    Args:
        date (str): Date in 'YYYY-MM-DD' format.
        time (str): Time in 'HH:MM' format.
    
    Returns:
        dict: 
            - status: 'free' | 'busy' | 'error'
            - confirmed: { 'date': ..., 'time': ... } if available
            - alternative: { 'date': ..., 'time': ... } if the original is not available
    """
    try:
        if check_availability_raw(date, time) == "free":
            return {
                "status": "free",
                "confirmed": {"date": date, "time": time},
                "alternative": None
            }

        current_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        for i in range(1, 24): 
            candidate_dt = current_dt + timedelta(minutes=30 * i)
            c_date = candidate_dt.strftime("%Y-%m-%d")
            c_time = candidate_dt.strftime("%H:%M")
            if check_availability_raw(c_date, c_time) == "free":
                return {
                    "status": "busy",
                    "confirmed": None,
                    "alternative": {"date": c_date, "time": c_time}
                }

        return {
            "status": "busy",
            "confirmed": None,
            "alternative": None
        }

    except Exception as e:
        print(f"Chyba v get_next_available_slot: {e}")
        return {
            "status": "error",
            "confirmed": None,
            "alternative": None
        }

    

class CalendarTools:
    def __init__(self):
        self.tools = [
            check_availability,
            get_next_available_slot
        ] + tools

    def get_tools(self):
        return self.tools