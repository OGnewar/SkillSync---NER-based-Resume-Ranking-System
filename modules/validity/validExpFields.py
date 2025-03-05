import re

def validateExpFields(exp_fields):
    """
    Validates extracted experience fields by checking:
    - The field contains only letters, spaces, and common symbols (e.g., & and -).
    - The field length is reasonable (2-50 characters).
    - The field is not just generic words (e.g., 'experience', 'field').
    """
    valid_fields = []
    
    # Define common invalid generic words
    invalid_keywords = {"experience", "field", "work", "role", "position", "job"}

    for field in exp_fields:
        field = field.strip()

        # Check if it contains only valid characters (letters, spaces, &, and -)
        if re.match(r"^[A-Za-z\s&\-]+$", field) and (2 <= len(field) <= 50):
            
            # Ensure it's not a generic word
            if field.lower() not in invalid_keywords:
                valid_fields.append(field)

    return valid_fields
