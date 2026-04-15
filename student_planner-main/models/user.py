import hashlib

def hash_password(password: str) -> str:
    """Returns a SHA-256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()


class User:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        student_id: str,
        password_hash: str,
        security_answers: list
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id
        self.password_hash = password_hash

        # Store answers in lowercase for comparison
        self.security_answers = [ans.lower() for ans in security_answers]

        # Display username (not used for login)
        self.username = f"{first_name} {last_name} {student_id}"

        # Core data
        self.tasks = []
        self.events = []
        self.reminders = []

        # Default preferences
        self.preferences = {
            "theme": "light",
            "layout": "list",
            "density": "normal"
        }

    def check_password(self, password: str) -> bool:
        return self.password_hash == hash_password(password)

    def add_task(self, task):
        self.tasks.append(task)

    def add_event(self, event_dict):
        self.events.append(event_dict)

    def add_reminder(self, reminder_dict):
        self.reminders.append(reminder_dict)