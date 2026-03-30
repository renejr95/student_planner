import hashlib


# ---------------------------
# PASSWORD HASHING
# ---------------------------
def hash_password(password: str) -> str:
    """Returns a SHA-256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()


class User:
    def __init__(self, username: str, password_hash: str):
        self.username = username              # stored lowercase
        self.password_hash = password_hash    # hashed password

        # Core data
        self.tasks = []                       # list of Task objects
        self.events = []                      # list of dicts
        self.reminders = []                   # list of dicts

        # Default preferences
        self.preferences = {
            "theme": "light",
            "layout": "list",
            "density": "normal"
        }

    # ---------------------------
    # PASSWORD CHECK
    # ---------------------------
    def check_password(self, password: str) -> bool:
        """Verifies a password against the stored hash."""
        return self.password_hash == hash_password(password)

    # ---------------------------
    # TASK MANAGEMENT
    # ---------------------------
    def add_task(self, task):
        self.tasks.append(task)

    # ---------------------------
    # EVENT MANAGEMENT
    # ---------------------------
    def add_event(self, event_dict):
        self.events.append(event_dict)

    # ---------------------------
    # REMINDER MANAGEMENT
    # ---------------------------
    def add_reminder(self, reminder_dict):
        self.reminders.append(reminder_dict)