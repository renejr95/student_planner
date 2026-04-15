from datetime import datetime
from utils.helpers import require_account, parse_due_date
from models.task import Task


class TaskManager:
    def __init__(self, storage, account_manager):
        self.storage = storage
        self.account = account_manager

    # ---------------------------
    # TASK MENU
    # ---------------------------
    def show_task_menu(self):
        while True:
            print("\n--- Task Menu ---")
            print("1. Add task")
            print("2. List tasks")
            print("3. Mark task done")
            print("4. Delete completed tasks")
            print("5. Delete a task")
            print("6. Edit a task")
            print("7. Organize task")
            print("8. Sort tasks")
            print("9. Search tasks")
            print("10. Back")

            option = input("Choose an option: ")

            if option == "1":
                self.add_task()
            elif option == "2":
                self.list_tasks()
            elif option == "3":
                self.mark_task_done()
            elif option == "4":
                self.delete_completed_tasks()
            elif option == "5":
                self.delete_task()
            elif option == "6":
                self.edit_task()
            elif option == "7":
                self.organize_task()
            elif option == "8":
                self.sort_tasks()
            elif option == "9":
                self.search_tasks()
            elif option == "10":
                return
            else:
                print("Invalid option.")

    # ---------------------------
    # TASK FUNCTIONS
    # ---------------------------

    def add_task(self):
        if not require_account(self.account):
            return

        title = input("Task title: ").strip()
        if not title:
            print("Task title cannot be empty.")
            return

        due_date = parse_due_date()

        task = Task(title, due_date.strftime("%m-%d-%y"))
        self.account.current_user.add_task(task)

        self.storage.save_data()
        print("Task added!")

    def list_tasks(self):
        if not require_account(self.account):
            return

        tasks = self.account.current_user.tasks

        if not tasks:
            print("No tasks yet.")
            return

        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task}")

    def mark_task_done(self):
        if not require_account(self.account):
            return

        self.list_tasks()
        tasks = self.account.current_user.tasks

        if not tasks:
            return

        try:
            choice = int(input("Which task number is done? "))
        except ValueError:
            print("Invalid input.")
            return

        if choice < 1 or choice > len(tasks):
            print("Invalid task number.")
            return

        task = tasks[choice - 1]

        if task.is_done:
            print("This task has already been completed.")
            return

        task.mark_done()
        self.storage.save_data()
        print("Task marked as done!")

    def delete_completed_tasks(self):
        if not require_account(self.account):
            return

        tasks = self.account.current_user.tasks
        completed = [t for t in tasks if t.is_done]

        if not completed:
            print("There are no completed tasks to delete.")
            return

        confirm = input(f"Delete all {len(completed)} completed tasks? (y/n): ").lower()
        if confirm != "y":
            print("Deletion canceled.")
            return

        self.account.current_user.tasks = [t for t in tasks if not t.is_done]
        self.storage.save_data()
        print("Completed tasks deleted!")

    def delete_task(self):
        if not require_account(self.account):
            return

        self.list_tasks()
        tasks = self.account.current_user.tasks

        if not tasks:
            return

        try:
            choice = int(input("Select task number to delete: "))
        except ValueError:
            print("Invalid input.")
            return

        if choice < 1 or choice > len(tasks):
            print("Invalid task number.")
            return

        task = tasks[choice - 1]

        confirm = input(f"Delete '{task.title}'? (y/n): ").lower()
        if confirm != "y":
            print("Deletion canceled.")
            return

        tasks.pop(choice - 1)
        self.storage.save_data()
        print("Task deleted!")

    def edit_task(self):
        if not require_account(self.account):
            return

        self.list_tasks()
        tasks = self.account.current_user.tasks

        if not tasks:
            return

        try:
            choice = int(input("Select task number to edit: "))
        except ValueError:
            print("Invalid input.")
            return

        if choice < 1 or choice > len(tasks):
            print("Invalid task number.")
            return

        task = tasks[choice - 1]

        if task.is_done:
            print("You cannot edit a completed task.")
            return

        print("Leave a field blank to keep the current value.")

        new_title = input(f"New title ({task.title}): ").strip()
        new_due = input(f"New due date ({task.due_date}) MM-DD-YY: ").strip()
        new_color = input(f"New color ({task.color}): ").strip()
        new_priority = input(f"New priority ({task.priority}): ").strip()

        if new_title:
            task.title = new_title

        if new_due:
            try:
                datetime.strptime(new_due, "%m-%d-%y")
                task.due_date = new_due
            except ValueError:
                print("Invalid date format. Keeping old date.")

        if new_color:
            task.color = new_color

        if new_priority:
            task.priority = new_priority

        self.storage.save_data()
        print("Task updated!")

    def organize_task(self):
        if not require_account(self.account):
            return

        self.list_tasks()
        tasks = self.account.current_user.tasks

        if not tasks:
            return

        try:
            choice = int(input("Select task number: "))
        except ValueError:
            print("Invalid input.")
            return

        if choice < 1 or choice > len(tasks):
            print("Invalid task number.")
            return

        task = tasks[choice - 1]

        if task.is_done:
            print("You cannot organize a completed task.")
            return

        color = input("Enter color label: ")
        priority = input("Priority (High/Medium/Low): ")

        task.set_color(color)
        task.set_priority(priority)

        self.storage.save_data()
        print("Task updated!")

    def sort_tasks(self):
        if not require_account(self.account):
            return

        print("1. Sort by due date")
        print("2. Sort by priority (High → Low)")
        choice = input("Choose sorting method: ")

        tasks = self.account.current_user.tasks

        if choice == "1":
            tasks.sort(key=lambda t: datetime.strptime(t.due_date, "%m-%d-%y"))
            print("Tasks sorted by due date.")

        elif choice == "2":
            priority_order = {"High": 1, "Medium": 2, "Low": 3, None: 4}
            tasks.sort(key=lambda t: priority_order.get(t.priority, 4))
            print("Tasks sorted by priority.")

        else:
            print("Invalid option.")
            return

        self.storage.save_data()

    def search_tasks(self):
        if not require_account(self.account):
            return

        keyword = input("Search keyword: ").lower()
        tasks = self.account.current_user.tasks

        results = [
            (i, t) for i, t in enumerate(tasks, start=1)
            if keyword in t.title.lower()
        ]

        if not results:
            print("No tasks found.")
            return

        print("Search results:")
        for i, task in results:
            print(f"{i}. {task}")