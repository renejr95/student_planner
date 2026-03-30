from utils.helpers import require_account


class EventManager:
    def __init__(self, storage, account_manager):
        self.storage = storage
        self.account = account_manager

    # ---------------------------
    # EVENT MENU
    # ---------------------------
    def show_event_menu(self):
        while True:
            print("\n--- Event Menu ---")
            print("1. Create event")
            print("2. Create reminder")
            print("3. Back")

            option = input("Choose an option: ")

            if option == "1":
                self.create_event()
            elif option == "2":
                self.create_reminder()
            elif option == "3":
                return
            else:
                print("Invalid option.")

    # ---------------------------
    # CREATE EVENT
    # ---------------------------
    def create_event(self):
        if not require_account(self.account):
            return

        title = input("Event title: ").strip()
        time = input("Event time: ").strip()
        location = input("Location: ").strip()

        if not title:
            print("Event must have a title.")
            return

        event = {
            "title": title,
            "time": time,
            "location": location
        }

        self.account.current_user.events.append(event)
        self.storage.save_data()

        print("Event created!")

    # ---------------------------
    # CREATE REMINDER
    # ---------------------------
    def create_reminder(self):
        if not require_account(self.account):
            return

        title = input("Reminder title: ").strip()
        date = input("Date (MM-DD-YY): ").strip()
        time = input("Time (HH:MM): ").strip()

        if not title:
            print("Reminder must have a title.")
            return

        reminder = {
            "title": title,
            "date": date,
            "time": time,
            "notify": True
        }

        self.account.current_user.reminders.append(reminder)
        self.storage.save_data()

        print("Reminder created!")