import re

def validateYears(exp_years):
    """
    Validates experience duration strings to ensure they match acceptable formats.
    """
    valid_formats = [
        r"^\d{4}\s*(?:-|–|to)\s*(\d{4}|Present|Ongoing)$",  # "2020-2024", "2020 to Present"
        r"^\w{3,9} \d{1,2}, \d{4}\s*(?:-|–|to)\s*(\w{3,9} \d{1,2}, \d{4}|Present|Ongoing)$",  # "Nov 10, 2020 to Dec 10, 2021"
        r"^\w{3,9} \d{1,2} \d{4}\s*(?:-|–|to)\s*(\w{3,9} \d{1,2} \d{4}|Present|Ongoing)$",  # ✅ NEW: "Sep 10 2020 - Nov 13 2025"
        r"^\d{2}/\d{2}/\d{4}\s*(?:-|–|to)\s*(\d{2}/\d{2}/\d{4}|Present|Ongoing)$",  # "05/13/2020 - 06/16/2021"
        r"^\d{1,2} \d{4}\s*(?:-|–|to)\s*\d{1,2} \d{4}$",  # "11 2024 to 12 2025"
        r"^\d+\s*(?:years?|yrs?)$",  # "3 years", "5 yrs"
        r"^\d+\+\s*(?:years?|yrs?)$",  # "4+ years"
        r"^(?:At least|Minimum|More than|Over|Up to|Approximately|Around)\s+\d+\s*(?:years?|yrs?)$",  # "At least 4 years"
        r"^(?:Between|From)\s+\d+\s*(?:years?|yrs?)\s*(?:and|to)\s*\d+\s*(?:years?|yrs?)$",  # "Between 3 and 5 years"
        r"^\d+\s*(?:to|-)\s*\d+\s*(?:years?|yrs?)$",  # "3 to 5 years"
    ]

    valid_exp = []
    for exp in exp_years:
        if any(re.match(pattern, exp.strip(), re.IGNORECASE) for pattern in valid_formats):
            valid_exp.append(exp)

    return valid_exp