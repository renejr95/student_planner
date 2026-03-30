from managers.account_manager import AccountManager
from managers.task_manager import TaskManager
from managers.event_manager import EventManager
from managers.preference_manager import PreferenceManager
from managers.storage_manager import StorageManager


def main():
    # Initialize storage
    storage = StorageManager()
    storage.load_data()

    # Initialize managers
    account = AccountManager(storage)
    tasks = TaskManager(storage, account)
    events = EventManager(storage, account)
    prefs = PreferenceManager(storage, account)

    # Main loop
    while True:
        # If no user is logged in → show login menu
        if account.current_user is None:
            if not account.show_login_menu():
                break  # Exit program

        # If user IS logged in → show main planner menu
        else:
            if not account.show_main_menu(tasks, events, prefs):
                break  # Exit program

    # Save before exiting
    storage.save_data()


if __name__ == "__main__":
    main()