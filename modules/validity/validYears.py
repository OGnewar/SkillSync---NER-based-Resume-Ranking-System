import re

def validateYears(exp_years):
    """
    Validates experience duration strings to ensure they match acceptable formats.
    """
    valid_formats = [
        r"^\d{4}\s*(?:-|–|to)\s*(\d{4}|Present|Ongoing)$",  # "2020-2024", "2020 to Present"

        # Full or short month name, optional day, year - separator - same format or Present/Ongoing
        r"^(?:\d{1,2}\s+)?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}\s*(?:-|–|to)\s*(?:(?:\d{1,2}\s+)?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}|Present|Ongoing)$",

        r"^\d{1,2}/\d{1,2}/\d{4}\s*(?:-|–|to)\s*(\d{1,2}/\d{1,2}/\d{4}|Present|Ongoing)$",  # "05/13/2020 - 06/16/2021"
        r"^\d{1,2} \d{4}\s*(?:-|–|to)\s*(\d{1,2} \d{4}|Present|Ongoing)$",  # "11 2024 to 12 2025"

        r"^\d+\s*(?:years?|yrs?)$",  # "3 years", "5 yrs"
        r"^\d+\+\s*(?:years?|yrs?)$",  # "4+ years"
        r"^(?:At least|Minimum|More than|Over|Up to|Approximately|Around)\s+\d+\s*(?:years?|yrs?)$",  # "At least 4 years"
        r"^(?:Between|From)\s+\d+\s*(?:years?|yrs?)\s*(?:and|to)\s*\d+\s*(?:years?|yrs?)$",  # "Between 3 and 5 years"
        r"^\d+\s*(?:to|-)\s*\d+\s*(?:years?|yrs?)$",  # "3 to 5 years"
    ]

    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in valid_formats]
    
    valid_exp = []
    for exp in exp_years:
        exp_clean = exp.strip()
        if any(pattern.match(exp_clean) for pattern in compiled_patterns):
            valid_exp.append(exp_clean)

    return valid_exp
