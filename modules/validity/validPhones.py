import re

def validatePhones(phone_list):
    """
    Validates phone numbers based on common formats, including:
    - International format: +1234567890, +1-234-567-890
    - Local format: (123) 456-7890, 123-456-7890
    - Spaced format: 123 456 7890
    """
    phone_pattern = r"^\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$"
    
    valid_phones = [phone for phone in phone_list if re.match(phone_pattern, phone)]
    
    return valid_phones
