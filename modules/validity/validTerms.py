import re

def validateTerms(skills):
    """
    Validates extracted hard skills by ensuring they contain only valid characters:
    - Letters, numbers, and common technical symbols (+, #, ., -, /, &).
    - No special characters like @, $, %, ^, *, etc.
    """
    valid_skills = []
    pattern = re.compile(r"^[a-zA-Z0-9+#.\-/& ]+$")  # Allowed characters

    for skill in skills:
        skill = skill.strip()

        # Check if the skill contains only valid characters
        if pattern.match(skill):
            valid_skills.append(skill)

    return valid_skills
