import tkinter as tk
from gui_main import StudentPlannerGUI


def main():
    root = tk.Tk()
    app = StudentPlannerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


