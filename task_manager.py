import json
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

class Task:
    def __init__(self, name, due_date, start_time=None, end_time=None, status="incomplete", priority="normal"):
        """
        Initialise une nouvelle tâche.
        """
        self.name = name
        self.due_date = due_date
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.priority = priority

    def get_duration(self):
        """
        Calcule et retourne la durée de la tâche si les heures de début et de fin sont spécifiées.
        """
        if self.start_time and self.end_time:
            start = datetime.strptime(self.start_time, '%H:%M')
            end = datetime.strptime(self.end_time, '%H:%M')
            return end - start
        return timedelta()

class TaskManager:
    def __init__(self, app):
        """
        Initialise le gestionnaire de tâches.
        """
        self.app = app
        self.current_project = None
        self.tasks_file = 'tasks.json'
        self.tasks_data = self.load_tasks()

    def create_task_interface(self):
        """
        Crée l'interface utilisateur pour la gestion des tâches.
        """
        self.app.auth_manager.clear_frames()
        self.app.auth_manager.task_frame.pack()

        tk.Label(self.app.auth_manager.task_frame, text="Gestion des Tâches", font=("Helvetica", 16)).pack(pady=10)

        self.app.auth_manager.project_menu = tk.StringVar(self.app.auth_manager.task_frame)
        self.app.auth_manager.project_menu.set(self.current_project.name if self.current_project else "")

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
        self.app.auth_manager.start_time.bind('<FocusOut>', self.format_time_entry)

        self.app.auth_manager.end_time = tk.Entry(self.app.auth_manager.task_frame)
        self.app.auth_manager.end_time.pack(pady=5)
        self.app.auth_manager.end_time.insert(0, "Heure de fin (HH:MM)")
        self.app.auth_manager.end_time.bind('<FocusOut>', self.format_time_entry)

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

        tk.Button(self.app.auth_manager.task_frame, text="Sauvegarder", command=self.save_tasks).pack(pady=5)

        self.update_task_listbox()

    def change_project(self, project_name):
        """
        Change le projet courant et met à jour la liste des tâches.
        """
        self.current_project = self.app.project_manager.projects.get(project_name, None)
        self.update_task_listbox()

    def add_task(self):
        """
        Ajoute une nouvelle tâche au projet courant.
        """
        task_name = self.app.auth_manager.task_name_entry.get()
        due_date = self.app.auth_manager.calendar.get_date()
        start_time = self.validate_and_format_time(self.app.auth_manager.start_time.get())
        end_time = self.validate_and_format_time(self.app.auth_manager.end_time.get())
        priority = self.app.auth_manager.priority_var.get()
        if task_name and self.current_project:
            new_task = Task(task_name, due_date, start_time, end_time, priority=priority)
            self.current_project.add_task(new_task)
            self.update_task_listbox()
            self.clear_task_entries()
        else:
            messagebox.showerror("Erreur", "Le nom de la tâche et la sélection d'un projet sont obligatoires")

    def modify_task(self):
        """
        Modifie les détails de la tâche sélectionnée.
        """
        selection = self.app.auth_manager.tasks_listbox.curselection()
        if selection:
            old_task_name = self.app.auth_manager.tasks_listbox.get(selection[0]).split(" - ")[0]
            new_task_name = self.app.auth_manager.task_name_entry.get()
            new_task_date = self.app.auth_manager.calendar.get_date()
            new_start_time = self.validate_and_format_time(self.app.auth_manager.start_time.get())
            new_end_time = self.validate_and_format_time(self.app.auth_manager.end_time.get())
            new_priority = self.app.auth_manager.priority_var.get()
            if new_task_name and self.current_project:
                self.current_project.update_task(old_task_name, new_task_name, new_task_date, new_start_time, new_end_time, new_priority)
                self.update_task_listbox()
                self.clear_task_entries()
            else:
                messagebox.showerror("Erreur", "Le nom de la tâche et la sélection d'un projet sont obligatoires")

    def remove_task(self):
        """
        Supprime la tâche sélectionnée.
        """
        selection = self.app.auth_manager.tasks_listbox.curselection()
        if selection:
            task_name = self.app.auth_manager.tasks_listbox.get(selection[0]).split(" - ")[0]
            if self.current_project:
                self.current_project.remove_task(task_name)
                self.update_task_listbox()

    def select_task(self, event):
        """
        Sélectionne une tâche de la liste des tâches et remplit les champs d'édition.
        """
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
        """
        Met à jour la liste des tâches lorsque la date sélectionnée change.
        """
        self.update_task_listbox()

    def update_task_listbox(self):
        """
        Met à jour la liste des tâches affichées et calcule la durée totale des tâches.
        """
        if hasattr(self.app.auth_manager, 'tasks_listbox') and self.app.auth_manager.tasks_listbox.winfo_exists():
            self.app.auth_manager.tasks_listbox.delete(0, tk.END)
            total_duration = timedelta()
            if self.current_project:
                for task in self.current_project.tasks:
                    self.app.auth_manager.tasks_listbox.insert(tk.END, f"{task.name} - {task.start_time} à {task.end_time} - {task.priority}")
                    total_duration += task.get_duration()
            self.total_duration_label.config(text=f"Durée totale des tâches : {total_duration}")

    def clear_task_entries(self):
        """
        Efface les champs d'entrée des tâches.
        """
        self.app.auth_manager.task_name_entry.delete(0, tk.END)
        self.app.auth_manager.start_time.delete(0, tk.END)
        self.app.auth_manager.end_time.delete(0, tk.END)
        self.app.auth_manager.priority_var.set("normal")

    def format_time_entry(self, event):
        """
        Formate les entrées de temps pour qu'elles soient au format HH:MM.
        """
        entry = event.widget
        time_str = entry.get().strip()
        formatted_time = self.validate_and_format_time(time_str)
        entry.delete(0, tk.END)
        entry.insert(0, formatted_time)

    def validate_and_format_time(self, time_str):
        """
        Valide et formate les entrées de temps au format HH:MM.
        """
        time_str = time_str.strip()
        if len(time_str) == 4 and time_str.isdigit():
            return f"{time_str[:2]}:{time_str[2:]}"
        elif len(time_str) == 3 and time_str.isdigit():
            return f"0{time_str[0]}:{time_str[1:]}"
        elif len(time_str) == 5 and ':' in time_str:
            try:
                datetime.strptime(time_str, '%H:%M')
                return time_str
            except ValueError:
                pass
        messagebox.showerror("Erreur", "L'heure doit être au format HH:MM")
        return ""

    def load_tasks(self):
        """
        Charge les tâches depuis un fichier JSON.
        """
        try:
            with open(self.tasks_file, "r") as tasks_file:
                tasks_data = json.load(tasks_file)
                return tasks_data.get(self.app.auth_manager.current_user, {"tasks": [], "projects": []})
        except (FileNotFoundError, json.JSONDecodeError):
            return {"tasks": [], "projects": []}

    def save_tasks(self):
        """
        Sauvegarde les tâches dans un fichier JSON.
        """
        print("Sauvegarde des tâches...")  # Debug message
        try:
            with open(self.tasks_file, "r") as tasks_file:
                tasks_data = json.load(tasks_file)
        except (FileNotFoundError, json.JSONDecodeError):
            tasks_data = {}

        if self.app.auth_manager.is_admin_user(self.app.auth_manager.current_user):
            tasks_data[self.app.auth_manager.current_user] = {
                "tasks": [task.__dict__ for project in self.app.project_manager.projects.values() for task in project.tasks],
                "projects": [project.name for project in self.app.project_manager.projects.values()]
            }
        else:
            user_tasks = {
                "tasks": [task.__dict__ for task in self.current_project.tasks] if self.current_project else [],
                "projects": [self.current_project.name] if self.current_project else []
            }
            tasks_data[self.app.auth_manager.current_user] = user_tasks

        with open(self.tasks_file, "w") as tasks_file:
            json.dump(tasks_data, tasks_file, indent=4)
        print("Tâches sauvegardées:", json.dumps(tasks_data, indent=4))  # Debug message

    def get_tasks(self, username):
        """
        Retourne les tâches d'un utilisateur spécifié.
        """
        if username in self.tasks_data:
            return self.tasks_data[username].get('tasks', [])
        return []

    def add_task_to_user(self, username, task):
        """
        Ajoute une tâche à l'utilisateur spécifié.
        """
        if username not in self.tasks_data:
            self.tasks_data[username] = {"tasks": [], "projects": []}
        self.tasks_data[username]['tasks'].append(task)
        self.save_tasks()

    def get_all_tasks(self):
        """
        Retourne toutes les tâches de tous les utilisateurs.
        """
        all_tasks = []
        for user, data in self.tasks_data.items():
            all_tasks.extend(data.get('tasks', []))
        return all_tasks

    def clear_tasks(self):
        """
        Efface toutes les tâches du projet courant.
        """
        if self.current_project:
            self.current_project.tasks = []
            self.update_task_listbox()
