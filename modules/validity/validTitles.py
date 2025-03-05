import re

def validateTitles(job_titles):
    valid_titles = []
    
    for title in job_titles:
        title = title.strip()
        
        # Regex: Allows letters, numbers, spaces, hyphens, ampersands, apostrophes, dots, commas, and slashes
        if re.fullmatch(r"[A-Za-z0-9&\-',./ ]{2,100}", title):
            valid_titles.append(title)
    
    return valid_titles
