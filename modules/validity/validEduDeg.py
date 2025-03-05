import re

def validateEduDeg(degrees):
    """
    Validates extracted education degrees by ensuring:
    - The degree follows common naming conventions.
    - Allows full names and abbreviations.
    - Handles different case formats.
    """
    valid_degrees = []

    # Common degree patterns
    degree_patterns = [
        r"(Bachelor|Master|Doctor|Ph\.?D\.?|Diploma|Associate)\s+(of\s+)?[A-Za-z\s]+",  # Full degree names
        r"\b(B\.?Sc|M\.?Sc|B\.?A|M\.?A|B\.?Tech|M\.?Tech|B\.?Eng|M\.?Eng|MBA|MPhil|BBA|LLB|LLM|MD|DDS|DMD|JD|EdD)\b",  # Common abbreviations
        r"\b(PhD|MSc|BSc|MA|BA|BS|MS|BE|ME|BEng|MEng|BBA|MBA|MPhil|LLB|LLM|MD|DDS|DMD|JD|EdD)\b",  # Variants without dots
        r"\b(High\s+School\s+Diploma|Associate\s+Degree)\b",  # Other valid degrees
    ]

    # Compile regex patterns
    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in degree_patterns]

    for degree in degrees:
        degree = degree.strip()

        # Check if it matches any valid degree pattern
        if any(pattern.match(degree) for pattern in compiled_patterns):
            valid_degrees.append(degree)

    return valid_degrees
