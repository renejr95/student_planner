import json
import os
from models.user import User
from models.task import Task


class StorageManager:
    def __init__(self):
        # Data containers
        self.users = {}              # student_id → User object
        self.current_user = None     # currently logged-in User
        self.login_attempts = {}     # student_id → failed attempts

        # File path
        self.data_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "user_data.json"
        )

    # ---------------------------
    # LOAD DATA
    # ---------------------------
    def load_data(self):
        if not os.path.exists(self.data_file):
            return

        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("Data file corrupted. Starting fresh.")
            return

        # Load users
        for u in data.get("users", []):
            # NEW FORMAT
            if "first_name" in u:
                user = User(
                    first_name=u["first_name"],
                    last_name=u["last_name"],
                    student_id=u["student_id"],
                    password_hash=u["password_hash"],
                    security_answers=u.get("security_answers", ["", "", ""])
                )

            # OLD FORMAT (username = "First Last ID")
            else:
                first, last, student_id = u["username"].split()
                user = User(
                    first_name=first,
                    last_name=last,
                    student_id=student_id,
                    password_hash=u["password_hash"],
                    security_answers=["", "", ""]
                )

            # Load tasks
            for t in u.get("tasks", []):
                task = Task(
                    t["title"],
                    t["due"],
                    t.get("color"),
                    t.get("priority")
                )
                if t.get("done"):
                    task.mark_done()
                user.tasks.append(task)

            # Load events
            user.events = u.get("events", [])

            # Load reminders
            user.reminders = u.get("reminders", [])

            # Load preferences
            user.preferences = u.get("preferences", user.preferences)

            # Store user by student_id
            self.users[user.student_id] = user

        # Load current user
        current_id = data.get("current_user")
        if current_id in self.users:
            self.current_user = self.users[current_id]

        # Load login attempts
        self.login_attempts = data.get("login_attempts", {})

    # ---------------------------
    # SAVE DATA
    # ---------------------------
    def save_data(self):
        data = {
            "users": [],
            "current_user": self.current_user.student_id if self.current_user else None,
            "login_attempts": self.login_attempts
        }

        for user in self.users.values():
            user_dict = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "student_id": user.student_id,
                "password_hash": user.password_hash,
                "security_answers": user.security_answers,
                "tasks": [
                    {
                        "title": t.title,
                        "due": t.due_date,
                        "done": t.is_done,
                        "color": t.color,
                        "priority": t.priority
                    }
                    for t in user.tasks
                ],
                "events": user.events,
                "reminders": user.reminders,
                "preferences": user.preferences
            }

            data["users"].append(user_dict)

        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)
