import re


# ---------------------------
# USERNAME VALIDATION
# ---------------------------
def validate_username(username: str):
    """
    Validates username format:
    FirstName LastName StudentID
    - First and last name capitalized
    - Student ID is digits only
    Returns (True, normalized_username) or (False, error_message)
    """

    pattern = r"^[A-Z][a-z]+ [A-Z][a-z]+ [0-9]+$"

    if not re.match(pattern, username):
        return False, (
            "Invalid format. Use: FirstName LastName StudentID "
            "(capitalized names, ID must be digits)."
        )

    return True, username.lower()


# ---------------------------
# PASSWORD VALIDATION
# ---------------------------
def validate_password(password: str, confirm: str):
    """
    Validates password rules:
    - Must match confirmation
    - At least 8 characters
    - Contains at least one letter
    - Contains at least one number
    Returns (True, password) or (False, error_message)
    """

    if password != confirm:
        return False, "Passwords do not match."

    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."

    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."

    return True, password