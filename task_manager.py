import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta

class Task:
    def __init__(self, name, due_date, start_time=None, end_time=None, status="incomplete", priority="normal"):
        self.name = name
        self.due_date = due_date
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.priority = priority

    def get_duration(self):
        if self.start_time and self.end_time:
            start = datetime.strptime(self.start_time, '%H:%M')
            end = datetime.strptime(self.end_time, '%H:%M')
            return end - start
        return timedelta()

class TaskManager:
    def __init__(self, app):
        self.app = app
        self.current_project = None

    def create_task_interface(self):
        self.app.auth_manager.clear_frames()
        self.app.auth_manager.task_frame.pack()

        tk.Label(self.app.auth_manager.task_frame, text="Gestion des Tâches", font=("Helvetica", 16)).pack(pady=10)

        self.app.auth_manager.project_menu = tk.StringVar(self.app.auth_manager.task_frame)
        self.app.auth_manager.project_menu.set("Select Project")

        self.app.auth_manager.project_dropdown = tk.OptionMenu(self.app.auth_manager.task_frame, self.app.auth_manager.project_menu, *self.app.project_manager.projects.keys(), command=self.change_project)
        self.app.auth_manager.project_dropdown.pack(pady=5)

        self.app.auth_manager.calendar = Calendar(self.app.auth_manager.task_frame, selectmode="day", date_pattern="dd/MM/yyyy")
        self.app.auth_manager.calendar.pack(pady=10)
        self.app.auth_manager.calendar.bind("<<CalendarSelected>>", self.date_selectionnee)

        self.app.auth_manager.task_name_entry = tk.Entry(self.app.auth_manager.task_frame)
        self.app.auth_manager.task_name_entry.pack(pady=5)
        self.app.auth_manager.task_name_entry.insert(0, "Nom de la tâche")

        self.app.auth_manager.start_time = tk.Entry(self.app.auth_manager.task_frame)
        self.app.auth_manager.start_time.pack(pady=5)
        self.app.auth_manager.start_time.insert(0, "Heure de début (HH:MM)")

        self.app.auth_manager.end_time = tk.Entry(self.app.auth_manager.task_frame)
        self.app.auth_manager.end_time.pack(pady=5)
        self.app.auth_manager.end_time.insert(0, "Heure de fin (HH:MM)")

        self.app.auth_manager.priority_var = tk.StringVar(self.app.auth_manager.task_frame)
        self.app.auth_manager.priority_var.set("normal")
        tk.Label(self.app.auth_manager.task_frame, text="Priorité:").pack(pady=5)
        tk.OptionMenu(self.app.auth_manager.task_frame, self.app.auth_manager.priority_var, "low", "normal", "high").pack(pady=5)

        tk.Button(self.app.auth_manager.task_frame, text="Ajouter Tâche", command=self.add_task).pack(pady=5)
        tk.Button(self.app.auth_manager.task_frame, text="Modifier Tâche", command=self.modify_task).pack(pady=5)

        self.app.auth_manager.tasks_listbox = tk.Listbox(self.app.auth_manager.task_frame, width=70, height=15)
        self.app.auth_manager.tasks_listbox.pack(pady=10, padx=10)
        self.app.auth_manager.tasks_listbox.bind("<<ListboxSelect>>", self.select_task)

        self.total_duration_label = tk.Label(self.app.auth_manager.task_frame, text="Durée totale des tâches : 0:00:00")
        self.total_duration_label.pack(pady=5)

        tk.Button(self.app.auth_manager.task_frame, text="Supprimer Tâche", command=self.remove_task).pack(pady=5)
        tk.Button(self.app.auth_manager.task_frame, text="Retour aux Projets", command=self.app.project_manager.create_project_interface).pack(pady=5)

        self.afficher_taches(self.app.auth_manager.calendar.get_date())

    def change_project(self, project_name):
        self.app.project_manager.save_projects()
        self.current_project = self.app.project_manager.projects[project_name]
        self.update_task_listbox()

    def add_task(self):
        task_name = self.app.auth_manager.task_name_entry.get()
        due_date = self.app.auth_manager.calendar.get_date()
        start_time = self.app.auth_manager.start_time.get()
        end_time = self.app.auth_manager.end_time.get()
        priority = self.app.auth_manager.priority_var.get()
        if task_name and self.current_project:
            new_task = Task(task_name, due_date, start_time, end_time, priority=priority)
            self.current_project.add_task(new_task)
            self.update_task_listbox()
            self.clear_task_entries()
        else:
            messagebox.showerror("Erreur", "Le nom de la tâche et la sélection d'un projet sont obligatoires")

    def modify_task(self):
        selection = self.app.auth_manager.tasks_listbox.curselection()
        if selection:
            old_task_name = self.app.auth_manager.tasks_listbox.get(selection[0]).split(" - ")[0]
            new_task_name = self.app.auth_manager.task_name_entry.get()
            new_task_date = self.app.auth_manager.calendar.get_date()
            new_start_time = self.app.auth_manager.start_time.get()
            new_end_time = self.app.auth_manager.end_time.get()
            new_priority = self.app.auth_manager.priority_var.get()
            if new_task_name and self.current_project:
                self.current_project.update_task(old_task_name, new_task_name, new_task_date, new_start_time, new_end_time, new_priority)
                self.update_task_listbox()
                self.clear_task_entries()
            else:
                messagebox.showerror("Erreur", "Le nom de la tâche et la sélection d'un projet sont obligatoires")

    def remove_task(self):
        selection = self.app.auth_manager.tasks_listbox.curselection()
        if selection:
            task_name = self.app.auth_manager.tasks_listbox.get(selection[0]).split(" - ")[0]
            self.current_project.remove_task(task_name)
            self.update_task_listbox()

    def select_task(self, event):
        selection = self.app.auth_manager.tasks_listbox.curselection()
        if selection:
            task_name = self.app.auth_manager.tasks_listbox.get(selection[0]).split(" - ")[0]
            task = next((task for task in self.current_project.tasks if task.name == task_name), None)
            if task:
                self.app.auth_manager.task_name_entry.delete(0, tk.END)
                self.app.auth_manager.task_name_entry.insert(0, task.name)
                self.app.auth_manager.start_time.delete(0, tk.END)
                self.app.auth_manager.start_time.insert(0, task.start_time if task.start_time else "")
                self.app.auth_manager.end_time.delete(0, tk.END)
                self.app.auth_manager.end_time.insert(0, task.end_time if task.end_time else "")
                self.app.auth_manager.priority_var.set(task.priority)
                self.app.auth_manager.calendar.selection_set(task.due_date)

    def date_selectionnee(self, event):
        self.update_task_listbox()

    def update_task_listbox(self):
        self.app.auth_manager.tasks_listbox.delete(0, tk.END)
        total_duration = timedelta()
        if self.current_project:
            for task in self.current_project.tasks:
                self.app.auth_manager.tasks_listbox.insert(tk.END, f"{task.name} - {task.start_time} à {task.end_time}")
                total_duration += task.get_duration()
        self.total_duration_label.config(text=f"Durée totale des tâches : {total_duration}")

    def clear_task_entries(self):
        self.app.auth_manager.task_name_entry.delete(0, tk.END)
        self.app.auth_manager.start_time.delete(0, tk.END)
        self.app.auth_manager.end_time.delete(0, tk.END)
        self.app.auth_manager.priority_var.set("normal")

    def afficher_taches(self, date):
        self.update_task_listbox()
