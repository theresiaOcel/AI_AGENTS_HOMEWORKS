from lecture1.ReactAgent.tools.mail_classifier_tools import load_emails, classify_emails
from lecture1.ReactAgent.tools.mail_important_tools import marks_mails_as_important
from lecture1.ReactAgent.tools.mail_reply_tools import reply_to_emails
from lecture1.ReactAgent.tools.mail_spam_tools import move_mails_to_trash
from lecture1.ReactAgent.tools.mail_unknown_tools import mark_unknown_email
from lecture1.ReactAgent.tools.schedule_meeting_tools import schedule_meetings

tools = [
    {
        "type": "function",
        "function": {
            "name" : "load_emails",
            "description": "Use this function to retrieve emails from a file. Return list of emails.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file"},
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "classify_emails",
            "description": "Use this function to classify emails into categories. Function expects an array of loaded emails.",
            "parameters": {
                "type": "object",
                "properties": {
                    "emails" : {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "List of emails object to classify."
                    },
                },
                "required": ["emails"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reply_to_emails",
            "description": "Use this function to reply to emails. The function expects a list of retrieved emails. The list should be obtained from categorized_emails and should be named auto-reply.",
            "parameters": {
                "type": "object",
                "properties": {
                    "emails" : {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "List of auto-reply emails to which an auto-reply can be generated."
                    },
                },
                "required": ["emails"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_meetings",
            "description": "Use this function to schedule appointments based on emails. The function expects a list of retrieved emails. The list should be retrieved from categorized_emails and should be named meetings.",
            "parameters": {
                "type": "object",
                "properties": {
                    "emails": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "subject": {"type": "string"},
                                "body": {"type": "string"},
                                "from": {"type": "string"},
                                "to": {"type": "string"},
                                "timestamp": {"type": "string"}
                            },
                            "required": ["subject", "body", "from"]
                        },
                        "description": "A list of emails that include a request to schedule an appointment."
                    }
                },
                "required": ["emails"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "move_mails_to_trash",
            "description": "Use this function to move spam emails to the trash. The function requires an array of emails that are classified as spam.",
            "parameters": {
                "type": "object",
                "properties": {
                    "emails": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "List of emails classified as spam to delete."
                    },
                },
                "required": ["emails"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "marks_mails_as_important",
            "description": "Use this function to mark emails as important. The function expects an array of emails that have been classified as important.",
            "parameters": {
                "type": "object",
                "properties": {
                    "emails": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "List of emails classified as important."
                    },
                },
                "required": ["emails"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mark_unknown_email",
            "description": "Use this function to mark emails as unknown. The function expects an array of emails that have been classified as unknown.",
            "parameters": {
                "type": "object",
                "properties": {
                    "emails": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "List of emails classified as unknown."
                    },
                },
                "required": ["emails"]
            }
        }
    },
]

available_functions = {
    "load_emails": load_emails,
    "classify_emails": classify_emails,
    "reply_to_emails": reply_to_emails,
    "schedule_meetings": schedule_meetings,
    "move_mails_to_trash": move_mails_to_trash,
    "mark_unknown_email": mark_unknown_email,
    "marks_mails_as_important": marks_mails_as_important
}

function_output_key = {
    "load_emails": "emails",
    "classify_emails": "categorized_emails"
}