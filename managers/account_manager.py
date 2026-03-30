import re
from models.user import User, hash_password


class AccountManager:
    def __init__(self, storage):
        self.storage = storage

    # ---------------------------
    # Properties
    # ---------------------------
    @property
    def current_user(self):
        return self.storage.current_user

    @current_user.setter
    def current_user(self, value):
        self.storage.current_user = value

    # ---------------------------
    # LOGIN MENU
    # ---------------------------
    def show_login_menu(self):
        print("\n--- Student Planner ---")
        print("1. Create account")
        print("2. Log in")
        print("3. Exit")

        option = input("Choose an option: ")

        if option == "1":
            self.create_account()
            return True
        elif option == "2":
            self.login()
            return True
        elif option == "3":
            return False
        else:
            print("Invalid option.")
            return True

    # ---------------------------
    # MAIN MENU (ROUTING ONLY)
    # ---------------------------
    def show_main_menu(self, tasks, events, prefs):
        print(f"\n--- Student Planner ({self.current_user.username}) ---")
        print("1. Task Menu")
        print("2. Event Menu")
        print("3. Preferences")
        print("4. Log out")
        print("5. Delete account")
        print("6. Exit")

        option = input("Choose an option: ")

        if option == "1":
            tasks.show_task_menu()
            return True

        elif option == "2":
            events.show_event_menu()
            return True

        elif option == "3":
            prefs.show_preferences_menu()
            return True

        elif option == "4":
            self.logout()
            return True

        elif option == "5":
            self.delete_account()
            return True

        elif option == "6":
            return False

        else:
            print("Invalid option.")
            return True

    # ---------------------------
    # ACCOUNT CREATION
    # ---------------------------
    def create_account(self):
        print("\n--- Create an Account ---")
        print("Requirements:")
        print("• First and Last name must be capitalized (Example: John Doe)")
        print("• Student ID must be digits only (Example: 123456)")
        print("• Password must be at least 8 characters, contain letters AND numbers")
        print("Format: FirstName LastName StudentID")
        print("Example:  John      Doe     123456\n")

        username = input("Enter your full name and student ID: ").strip()

        # Validate username format
        pattern = r"^[A-Z][a-z]+ [A-Z][a-z]+ [0-9]+$"
        if not re.match(pattern, username):
            print("Invalid format. Use: FirstName LastName StudentID (capitalized names).")
            return

        username_key = username.lower()

        if username_key in self.storage.users:
            print("An account with this name already exists.")
            return

        # -------------------------
        # PASSWORD CREATION LOOP
        # -------------------------
        attempts = 0
        max_attempts = 5

        while attempts < max_attempts:
            password = input("Create a password: ").strip()
            confirm = input("Confirm password: ").strip()

            if password != confirm:
                print("Passwords do not match.")
                attempts += 1
                continue

            if len(password) < 8:
                print("Password must be at least 8 characters long.")
                attempts += 1
                continue

            if not re.search(r"[A-Za-z]", password):
                print("Password must contain at least one letter.")
                attempts += 1
                continue

            if not re.search(r"[0-9]", password):
                print("Password must contain at least one number.")
                attempts += 1
                continue

            break

        if attempts >= max_attempts:
            print("Too many invalid password attempts. Account creation canceled.")
            return

        # Create account
        password_hash = hash_password(password)
        user = User(username_key, password_hash)

        self.storage.users[username_key] = user
        self.storage.login_attempts[username_key] = 0
        self.current_user = user

        self.storage.save_data()
        print(f"Account created and logged in as {username}")

    # ---------------------------
    # LOGIN
    # ---------------------------
    def login(self):
        username = input("Enter username (First Last ID): ").strip().lower()

        if username not in self.storage.users:
            print("No such user.")
            return

        # Lockout check
        if self.storage.login_attempts.get(username, 0) >= 5:
            print("This account is locked due to too many failed login attempts.")
            return

        password = input("Enter password: ")
        user = self.storage.users[username]

        if not user.check_password(password):
            self.storage.login_attempts[username] += 1
            remaining = 5 - self.storage.login_attempts[username]

            if remaining > 0:
                print(f"Incorrect password. {remaining} attempts remaining.")
            else:
                print("Too many failed attempts. Your account is now locked.")

            self.storage.save_data()
            return

        # Successful login
        self.storage.login_attempts[username] = 0
        self.current_user = user
        self.storage.save_data()
        print(f"Logged in as {username}")

    # ---------------------------
    # LOGOUT
    # ---------------------------
    def logout(self):
        print(f"Logged out {self.current_user.username}")
        self.current_user = None
        self.storage.save_data()

    # ---------------------------
    # DELETE ACCOUNT
    # ---------------------------
    def delete_account(self):
        confirm = input(
            f"Are you sure you want to delete your account '{self.current_user.username}'? (y/n): "
        ).lower()

        if confirm != "y":
            print("Account deletion canceled.")
            return

        username = self.current_user.username

        del self.storage.users[username]
        del self.storage.login_attempts[username]

        self.current_user = None
        self.storage.save_data()

        print("Your account has been deleted.")