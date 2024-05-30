import tkinter as tk
from tkcalendar import Calendar

class CalendarManager:
    def __init__(self, app):
        self.app = app

    def create_calendar(self, frame):
        self.calendar = Calendar(frame, selectmode="day", date_pattern="dd/MM/yyyy")
        self.calendar.pack(pady=10)
        self.calendar.bind("<<CalendarSelected>>", self.date_selected)

    def date_selected(self, event):
        self.app.task_manager.update_task_listbox()
