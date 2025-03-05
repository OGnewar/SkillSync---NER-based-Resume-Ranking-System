import re

def validateEduFields(edu_fields):
    """
    Validates extracted education fields by ensuring:
    - The field contains only valid characters (letters, spaces, and hyphens).
    - The field length is reasonable (2-50 characters).
    - The field matches common academic fields.
    """
    valid_fields = []
    
    # Define a regex pattern to allow only valid characters
    field_pattern = re.compile(r"^[A-Za-z\s\-]+$")

    for field in edu_fields:
        field = field.strip()

        # Check if it matches the pattern and has a reasonable length
        if field_pattern.match(field) and (2 <= len(field) <= 50):
            valid_fields.append(field)

    return valid_fields
