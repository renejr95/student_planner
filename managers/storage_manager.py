import json
import os
from models.user import User
from models.task import Task


class StorageManager:
    def __init__(self):
        # Data containers
        self.users = {}              # username → User object
        self.current_user = None     # currently logged-in User
        self.login_attempts = {}     # username → failed attempts

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
            user = User(u["username"], u["password_hash"])

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

            self.users[user.username] = user

        # Load current user
        username = data.get("current_user")
        if username in self.users:
            self.current_user = self.users[username]

        # Load login attempts
        self.login_attempts = data.get("login_attempts", {})

    # ---------------------------
    # SAVE DATA
    # ---------------------------
    def save_data(self):
        data = {
            "users": [],
            "current_user": self.current_user.username if self.current_user else None,
            "login_attempts": self.login_attempts
        }

        for user in self.users.values():
            user_dict = {
                "username": user.username,
                "password_hash": user.password_hash,
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