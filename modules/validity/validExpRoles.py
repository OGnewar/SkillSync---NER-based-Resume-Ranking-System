import re

def validateExpRoles(exp_roles):
    """
    Validates extracted job roles by ensuring:
    - The role consists of alphabetic characters (with optional hyphens or spaces).
    - It does not contain numbers or unusual symbols.
    - It is not excessively short (e.g., less than 2 characters).
    """
    role_pattern = r"^[A-Za-z\s\-\/&]+$"
    
    valid_roles = [role for role in exp_roles if re.match(role_pattern, role) and len(role) > 2]
    
    return valid_roles
