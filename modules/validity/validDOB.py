from datetime import datetime
import re

def validateDOB(dob_list):
    """
    Validates extracted dates of birth (DOB) by checking:
    - Common date formats (YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY, etc.).
    - The person is between 15 and 100 years old.
    """
    valid_dobs = []
    current_year = datetime.now().year

    # Define common date formats
    date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y",
                    "%B %d, %Y", "%d %B %Y", "%b %d, %Y", "%d %b %Y"]

    for dob in dob_list:
        dob = dob.strip()
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(dob, fmt)
                age = current_year - parsed_date.year

                if 15 <= age <= 100:  # Ensure realistic age range
                    valid_dobs.append(dob)
                    break  # If valid, move to the next DOB

            except ValueError:
                continue  # Try the next format if parsing fails

    return valid_dobs
