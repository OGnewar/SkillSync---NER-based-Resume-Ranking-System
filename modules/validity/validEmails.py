import re

def validateEmails(email_list):
    """
    Validates email addresses to ensure they match standard email formats.
    """
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    valid_emails = [email for email in email_list if re.match(email_pattern, email)]
    
    return valid_emails
