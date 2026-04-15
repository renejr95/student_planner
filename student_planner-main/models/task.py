class Task:
    def __init__(self, title, due_date, color=None, priority=None):
        self.title = title
        self.due_date = due_date
        self.is_done = False
        self.color = color
        self.priority = priority

    def mark_done(self):
        self.is_done = True

    def set_color(self, color):
        self.color = color

    def set_priority(self, priority):
        self.priority = priority

    def __str__(self):
        status = "✓" if self.is_done else "✗"
        color_info = f" | Color: {self.color}" if self.color else ""
        priority_info = f" | Priority: {self.priority}" if self.priority else ""
        return f"{self.title} (Due: {self.due_date}) [{status}]{color_info}{priority_info}"