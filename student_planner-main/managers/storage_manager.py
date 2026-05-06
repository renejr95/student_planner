from pymongo import MongoClient
from models.user import User
from models.task import Task


class StorageManager:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.login_attempts = {}

        self.client = MongoClient(
            "mongodb+srv://ashlyperezs125_db_user:TdpHVbFBExEWpVh7@cluster0.pgtpkin.mongodb.net/?appName=Cluster0"
        )

        self.db = self.client["student_planner"]
        self.users_collection = self.db["users"]
        self.app_collection = self.db["app_data"]

        self.load_data()

    def load_data(self):
        self.users.clear()

        for u in self.users_collection.find():
            user = User(
                u["username"],
                u["password_hash"]
            )

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

            user.events = u.get("events", [])
            user.reminders = u.get("reminders", [])
            user.preferences = u.get("preferences", user.preferences)

            self.users[user.username] = user

        app_data = self.app_collection.find_one({"type": "settings"})

        if app_data:
            self.login_attempts = app_data.get("login_attempts", {})

            current_username = app_data.get("current_user")
            if current_username in self.users:
                self.current_user = self.users[current_username]

    def save_data(self):
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

            self.users_collection.update_one(
                {"username": user.username},
                {"$set": user_dict},
                upsert=True
            )

        self.app_collection.update_one(
            {"type": "settings"},
            {
                "$set": {
                    "type": "settings",
                    "current_user": self.current_user.username if self.current_user else None,
                    "login_attempts": self.login_attempts
                }
            },
            upsert=True
        )
