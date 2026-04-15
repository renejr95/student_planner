from datetime import datetime


# ---------------------------
# REQUIRE ACCOUNT
# ---------------------------
def require_account(account_manager):
    """
    Ensures a user is logged in before performing an action.
    Returns True if allowed, False if blocked.
    """
    if account_manager.current_user is None:
        print("You must be logged in first.")
        return False
    return True


# ---------------------------
# PARSE DUE DATE
# ---------------------------
def parse_due_date():
    """
    Prompts the user for a due date in MM-DD-YY format.
    Ensures the date is valid and not in the past.
    Returns a datetime.date object.
    """
    while True:
        due_str = input("Due date (MM-DD-YY): ").strip()

        try:
            due_date = datetime.strptime(due_str, "%m-%d-%y").date()
        except ValueError:
            print("Invalid date format. Please use MM-DD-YY.")
            continue

        if due_date < datetime.today().date():
            print("Due date cannot be in the past.")
            continue

        return due_date