import re

def validateNames(names):
    valid_names = []
    
    for name in names:
        name = name.strip()
        
        # Regex: Allows alphabets, spaces, hyphens, and apostrophes (e.g., "Jean-Pierre O'Connor")
        if re.fullmatch(r"[A-Za-z][A-Za-z' -]{1,49}", name):
            valid_names.append(name)
    
    return valid_names
