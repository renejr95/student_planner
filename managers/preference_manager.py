from utils.helpers import require_account


class PreferenceManager:
    def __init__(self, storage, account_manager):
        self.storage = storage
        self.account = account_manager

    # ---------------------------
    # PREFERENCES MENU
    # ---------------------------
    def show_preferences_menu(self):
        while True:
            print("\n--- Preferences ---")
            print("1. Theme (light/dark)")
            print("2. Layout (list/calendar)")
            print("3. Density (normal/compact)")
            print("4. Back")

            option = input("Choose an option: ")

            if option == "1":
                self.change_theme()
            elif option == "2":
                self.change_layout()
            elif option == "3":
                self.change_density()
            elif option == "4":
                return
            else:
                print("Invalid option.")

    # ---------------------------
    # THEME
    # ---------------------------
    def change_theme(self):
        if not require_account(self.account):
            return

        theme = input("Choose theme (light/dark): ").strip().lower()

        if theme not in ["light", "dark"]:
            print("Invalid theme.")
            return

        self.account.current_user.preferences["theme"] = theme
        self.storage.save_data()
        print("Theme updated!")

    # ---------------------------
    # LAYOUT
    # ---------------------------
    def change_layout(self):
        if not require_account(self.account):
            return

        layout = input("Choose layout (list/calendar): ").strip().lower()

        if layout not in ["list", "calendar"]:
            print("Invalid layout.")
            return

        self.account.current_user.preferences["layout"] = layout
        self.storage.save_data()
        print("Layout updated!")

    # ---------------------------
    # DENSITY
    # ---------------------------
    def change_density(self):
        if not require_account(self.account):
            return

        density = input("Choose density (normal/compact): ").strip().lower()

        if density not in ["normal", "compact"]:
            print("Invalid density.")
            return

        self.account.current_user.preferences["density"] = density
        self.storage.save_data()
        print("Density updated!")