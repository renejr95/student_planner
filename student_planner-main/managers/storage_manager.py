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

    # ---------------------------
    # LOAD DATA FROM MONGODB
    # ---------------------------
    def load_data(self):
        self.users.clear()
        self.current_user = None

        for u in self.users_collection.find():
            try:
                # Format 1: newer format
                if "first_name" in u and "last_name" in u and "student_id" in u:
                    first_name = u.get("first_name", "")
                    last_name = u.get("last_name", "")
                    student_id = u.get("student_id", "")

                # Format 2: username format like "Ash P 09876547"
                elif "username" in u:
                    parts = u["username"].split()

                    if len(parts) < 3:
                        print("Skipping invalid user:", u)
                        continue

                    first_name = parts[0]
                    last_name = parts[1]
                    student_id = parts[2]

                else:
                    print("Skipping old invalid user document:", u)
                    continue

                password_hash = u.get("password_hash")
                if not password_hash:
                    print("Skipping user without password hash:", u)
                    continue

                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    student_id=student_id,
                    password_hash=password_hash,
                    security_answers=u.get("security_answers", ["", "", ""])
                )

                # Load tasks
                for t in u.get("tasks", []):
                    try:
                        task = Task(
                            t.get("title", ""),
                            t.get("due", ""),
                            t.get("color"),
                            t.get("priority")
                        )

                        if t.get("done"):
                            task.mark_done()

                        user.tasks.append(task)

                    except Exception as e:
                        print("Skipping invalid task:", e)

                user.events = u.get("events", [])
                user.reminders = u.get("reminders", [])
                user.preferences = u.get("preferences", user.preferences)

                self.users[user.student_id] = user

            except Exception as e:
                print("Skipping user because of error:", e)

        # Load app settings
        app_data = self.app_collection.find_one({"type": "settings"})

        if app_data:
            self.login_attempts = app_data.get("login_attempts", {})

            current_id = app_data.get("current_user")
            if current_id in self.users:
                self.current_user = self.users[current_id]

    # ---------------------------
    # SAVE DATA TO MONGODB
    # ---------------------------
    def save_data(self):
        for user in self.users.values():

            user_dict = {
                "first_name": getattr(user, "first_name", ""),
                "last_name": getattr(user, "last_name", ""),
                "student_id": getattr(user, "student_id", ""),
                "username": getattr(user, "username", ""),
                "password_hash": getattr(user, "password_hash", ""),

                # IMPORTANT: saves security questions/answers safely
                "security_answers": getattr(user, "security_answers", ["", "", ""]),

                "tasks": [
                    {
                        "title": getattr(t, "title", ""),
                        "due": getattr(t, "due_date", ""),
                        "done": getattr(t, "is_done", False),
                        "color": getattr(t, "color", None),
                        "priority": getattr(t, "priority", None)
                    }
                    for t in getattr(user, "tasks", [])
                ],

                "events": getattr(user, "events", []),
                "reminders": getattr(user, "reminders", []),
                "preferences": getattr(user, "preferences", {})
            }

            self.users_collection.update_one(
                {"student_id": user_dict["student_id"]},
                {"$set": user_dict},
                upsert=True
            )

        self.app_collection.update_one(
            {"type": "settings"},
            {
                "$set": {
                    "type": "settings",
                    "current_user": self.current_user.student_id if self.current_user else None,
                    "login_attempts": self.login_attempts
                }
            },
            upsert=True
        )
