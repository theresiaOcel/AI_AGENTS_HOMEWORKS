from langchain.tools import tool
from .classifier import EmailClassifier
from .extractor import EmailExtractor
from .auto_replier import EmailReplier

from langchain_google_community.gmail.toolkit import GmailToolkit
from langchain_google_community.gmail.utils import (
    get_gmail_credentials,
    build_resource_service,
)

import os
import json
from datetime import datetime

CREDENTIALS_PATH = "lecture7/credentials/google_calendar_credential.json"
TOKEN_PATH = "lecture7/credentials/tokens/gmail_token.json"

credentials = get_gmail_credentials(
    token_file=TOKEN_PATH,
    client_secrets_file=CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/gmail.send"])

api_resource = build_resource_service(credentials=credentials)

toolkit = GmailToolkit(api_resource=api_resource)
tools = toolkit.get_tools()


@tool
def classify_email(email: str) -> str:
    """Classifies an email into a category based on its content.
    
    Possible categories: 'meeting', 'auto-reply', 'spam', 'important', 'unknown'.
    
    Args:
        email (str): The content of the email to classify.
        
    Returns:
        str: The category of the email."""
    
    print(f"[TOOL classify_email] Classifying email...")
    
    classifier = EmailClassifier()
    category  = classifier.classify(email=email)
    print(f"[TOOL classify_email] Classified email as: {category}")
    return category

@tool
def extract_meeting_details(email:str) -> dict:
    """Extracts meeting detail (date, time, participants) from email text.
    
    Return: {"date": "...", "time": "...", "participants": ["..."]}"""

    print(f"[TOOL extract_meeting_details] Extracting meeting details from email...")
    extractor = EmailExtractor()
    details = extractor.extract(email=email)
    print(f"[TOOL extract_meeting_details] Extracted details: {details}")
    return details

@tool
def prepare_email_for_moving(email_id: str, from_email:str, subject: str, body: str) -> dict:           
    """Prepares an email for moving to a specific folder.
    
    Args:
        email_id (str): Unique identifier of the email.
        from_email (str): Sender's email address.
        subject (str): Subject of the email.
        body (str): Body content of the email.
        
    Returns:
        dict: A dictionary containing all information about the email."""
    
    return {
        "email_id": email_id,
        "from": from_email,
        "subject": subject,
        "body": body
    }

@tool
def move_email(email: dict, folder_name: str) -> str:
    """Move an email to a specified folder.
    
    Args:
       email: A dictionary containing all information about the email (e.g., email_id, from, subject, body).
       folder_name: Name of folder where email should be moved.
    
    Returns:
        str: Confirmation message indicating the email has been moved."""
    
    try:
        base_dir = "lecture7/data_outputs"
        subfolder = os.path.join(base_dir, folder_name.lower())
        os.makedirs(subfolder, exist_ok=True)

        now = datetime.now().strftime("%Y%m%d_%H%M")
        log_filename = f"log_{now}.jsonl"
        log_path = os.path.join(subfolder, log_filename)

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(email, ensure_ascii=False) + "\n")

        return f"Email {email.get('email_id', '')} was logged to '{folder_name}' as JSON."

    except Exception as e:
        return f"Error while writing to JSONL: {e}"
    

@tool
def auto_reply_email(email: dict) -> str:
    """Replies to an email using a pre-defined template based on the FAQ database.
    
    Args:
        email (dict): A dictionary containing the email details (subject, from, body).
        
    Returns:
        str: The auto-reply message or '__NO_REPLY__' if no suitable reply is found."""
    
    replier = EmailReplier()
    response = replier.auto_reply(email=email)
    return response


class EmailTools:
    def __init__(self):
        self.tools = [
            classify_email,
            extract_meeting_details,
            move_email,
            auto_reply_email,
            prepare_email_for_moving
        ] + toolkit.get_tools()
    
    def get_tools(self):
        return self.tools