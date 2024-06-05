import json
from tkinter import messagebox, Toplevel
import tkinter as tk
from task_manager import Task

class Project:
    def __init__(self, name, priority="normal"):
        """
        Initialise un nouveau projet.
        """
        self.name = name
        self.priority = priority
        self.tasks = []

    def add_task(self, task):
        """
        Ajoute une tâche au projet.
        """
        self.tasks.append(task)

    def remove_task(self, task_name):
        """
        Supprime une tâche du projet par son nom.
        """
        self.tasks = [task for task in self.tasks if task.name != task_name]

    def update_task(self, old_task_name, new_task_name, new_task_date, new_start_time, new_end_time, new_priority):
        """
        Met à jour les informations d'une tâche existante dans le projet.
        """
        for task in self.tasks:
            if task.name == old_task_name:
                task.name = new_task_name
                task.due_date = new_task_date
                task.start_time = new_start_time
                task.end_time = new_end_time
                task.priority = new_priority
                break

    def update_priority(self, new_priority):
        """
        Met à jour la priorité du projet.
        """
        self.priority = new_priority

class ProjectManager:
    def __init__(self, app):
        """
        Initialise le gestionnaire de projets.
        """
        self.app = app
        self.projects = {}
        self.current_project = None

    def create_project_interface(self):
        """
        Crée l'interface utilisateur pour la gestion des projets.
        """
        self.app.auth_manager.clear_frames()
        self.app.auth_manager.project_frame.pack()

        tk.Label(self.app.auth_manager.project_frame, text="Sélectionnez ou Créez un Projet", font=("Helvetica", 16)).pack(pady=10)
        
        self.app.auth_manager.project_name_entry = tk.Entry(self.app.auth_manager.project_frame)
        self.app.auth_manager.project_name_entry.pack(pady=5)
        self.app.auth_manager.project_name_entry.insert(0, "Nom du projet")

        self.app.auth_manager.project_priority_var = tk.StringVar(self.app.auth_manager.project_frame)
        self.app.auth_manager.project_priority_var.set("normal")
        tk.Label(self.app.auth_manager.project_frame, text="Priorité:").pack(pady=5)
        tk.OptionMenu(self.app.auth_manager.project_frame, self.app.auth_manager.project_priority_var, "low", "normal", "high").pack(pady=5)

        tk.Button(self.app.auth_manager.project_frame, text="Créer Projet", command=self.create_project).pack(pady=5)

        self.app.auth_manager.project_listbox = tk.Listbox(self.app.auth_manager.project_frame, width=50, height=15)
        self.app.auth_manager.project_listbox.pack(pady=10, padx=10)
        self.app.auth_manager.project_listbox.bind("<<ListboxSelect>>", self.on_project_select)

        self.modify_button = tk.Button(self.app.auth_manager.project_frame, text="Modifier Projet", command=self.modify_project)
        self.modify_button.pack(pady=5)
        self.modify_button.config(state=tk.DISABLED)

        self.delete_button = tk.Button(self.app.auth_manager.project_frame, text="Supprimer Projet", command=self.delete_project)
        self.delete_button.pack(pady=5)
        self.delete_button.config(state=tk.DISABLED)

        self.access_tasks_button = tk.Button(self.app.auth_manager.project_frame, text="Accéder aux Tâches", command=self.access_tasks)
        self.access_tasks_button.pack(pady=5)
        self.access_tasks_button.config(state=tk.DISABLED)

        tk.Button(self.app.auth_manager.project_frame, text="Sauvegarder", command=self.save_projects).pack(pady=5)

        tk.Button(self.app.auth_manager.project_frame, text="Modifier Profil", command=self.app.user_manager.modify_profile).pack(pady=5)
        tk.Button(self.app.auth_manager.project_frame, text="Supprimer Profil", command=self.app.user_manager.delete_profile).pack(pady=5)
        tk.Button(self.app.auth_manager.project_frame, text="Se Déconnecter", command=self.logout).pack(pady=5)

        if self.app.auth_manager.is_admin_user(self.app.auth_manager.current_user):
            tk.Button(self.app.auth_manager.project_frame, text="Accéder à l'Admin", command=self.app.admin_manager.create_admin_interface).pack(pady=5)

        self.update_project_listbox()

    def create_project(self):
        """
        Crée un nouveau projet avec les informations fournies.
        """
        project_name = self.app.auth_manager.project_name_entry.get()
        project_priority = self.app.auth_manager.project_priority_var.get()
        if project_name:
            self.projects[project_name] = Project(project_name, priority=project_priority)
            self.update_project_listbox()
            self.update_project_menu()
            self.app.auth_manager.project_name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", "Le nom du projet ne peut pas être vide")

    def on_project_select(self, event):
        """
        Sélectionne un projet dans la liste des projets.
        """
        selection = self.app.auth_manager.project_listbox.curselection()
        if selection:
            project_name = self.app.auth_manager.project_listbox.get(selection[0]).split(" - ")[0]
            if project_name in self.projects:
                self.current_project = self.projects[project_name]
                self.modify_button.config(state=tk.NORMAL)
                self.delete_button.config(state=tk.NORMAL)
                self.access_tasks_button.config(state=tk.NORMAL)
            else:
                self.current_project = None
                self.modify_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)
                self.access_tasks_button.config(state=tk.DISABLED)

    def modify_project(self):
        """
        Modifie les informations du projet sélectionné.
        """
        if self.current_project:
            self.show_modify_project_window()

    def show_modify_project_window(self):
        """
        Affiche une fenêtre pour modifier les détails du projet.
        """
        modify_window = Toplevel(self.app.root)
        modify_window.title("Modifier Projet")
        
        tk.Label(modify_window, text="Nouveau nom du projet:").pack(pady=5)
        new_name_entry = tk.Entry(modify_window)
        new_name_entry.pack(pady=5)
        new_name_entry.insert(0, self.current_project.name)
        
        tk.Label(modify_window, text="Nouvelle priorité:").pack(pady=5)
        new_priority_var = tk.StringVar(modify_window)
        new_priority_var.set(self.current_project.priority)
        tk.OptionMenu(modify_window, new_priority_var, "low", "normal", "high").pack(pady=5)
        
        def save_changes():
            """
            Sauvegarde les modifications du projet.
            """
            new_project_name = new_name_entry.get()
            new_project_priority = new_priority_var.get()
            if new_project_name and new_project_name != self.current_project.name:
                self.projects[new_project_name] = self.projects.pop(self.current_project.name)
                self.current_project = self.projects[new_project_name]
                self.current_project.name = new_project_name
            if new_project_priority:
                self.current_project.update_priority(new_project_priority)
            self.update_project_listbox()
            self.update_project_menu()
            modify_window.destroy()
        
        tk.Button(modify_window, text="Sauvegarder", command=save_changes).pack(pady=5)

    def delete_project(self):
        """
        Supprime le projet sélectionné.
        """
        if self.current_project:
            confirm = messagebox.askyesno("Supprimer Projet", f"Êtes-vous sûr de vouloir supprimer le projet {self.current_project.name}?")
            if confirm:
                del self.projects[self.current_project.name]
                self.current_project = None
                self.update_project_listbox()
                self.update_project_menu()
                self.modify_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)
                self.access_tasks_button.config(state=tk.DISABLED)

    def access_tasks(self):
        """
        Accède aux tâches du projet sélectionné.
        """
        if self.current_project:
            self.app.task_manager.current_project = self.current_project
            self.app.task_manager.create_task_interface()
            self.app.task_manager.load_tasks()
        else:
            print("Aucun projet sélectionné pour accéder aux tâches.")

    def update_project_listbox(self):
        """
        Met à jour la liste des projets affichés.
        """
        if hasattr(self.app.auth_manager, 'project_listbox') and self.app.auth_manager.project_listbox.winfo_exists():
            self.app.auth_manager.project_listbox.delete(0, tk.END)
            for project_name, project in self.projects.items():
                self.app.auth_manager.project_listbox.insert(tk.END, f"{project_name} - {project.priority}")

    def update_project_menu(self):
        """
        Met à jour le menu déroulant des projets.
        """
        if hasattr(self.app.auth_manager, 'project_dropdown'):
            menu = self.app.auth_manager.project_dropdown["menu"]
            if menu:
                menu.delete(0, 'end')
                for project_name in self.projects.keys():
                    menu.add_command(label=project_name, command=lambda value=project_name: self.app.auth_manager.project_menu.set(value))

    def load_projects(self):
        """
        Charge les projets depuis un fichier JSON.
        """
        print("Chargement des projets...")  # Debug message
        self.projects = {}  # Clear current projects before loading new ones
        try:
            with open("projects.json", "r") as projects_file:
                projects_data = json.load(projects_file)
                print(f"Projets chargés depuis JSON: {projects_data}")  # Debug message
                if self.app.auth_manager.is_admin_user(self.app.auth_manager.current_user):
                    for user, user_projects in projects_data.items():
                        for project_name, project_data in user_projects.items():
                            if isinstance(project_data, dict):  # Check if project_data is a dictionary
                                project = Project(project_name, project_data.get('priority', 'normal'))
                                for task_data in project_data.get('tasks', []):
                                    task = Task(**task_data)
                                    project.add_task(task)
                                self.projects[project_name] = project
                            else:
                                print(f"Projet ignoré: {project_name} n'est pas un dictionnaire.")
                else:
                    user_projects = projects_data.get(self.app.auth_manager.current_user, {})
                    print(f"Projets utilisateur chargés depuis JSON: {user_projects}")  # Debug message
                    for project_name, project_data in user_projects.items():
                        if isinstance(project_data, dict):  # Check if project_data is a dictionary
                            project = Project(project_name, project_data.get('priority', 'normal'))
                            for task_data in project_data.get('tasks', []):
                                task = Task(**task_data)
                                project.add_task(task)
                            self.projects[project_name] = project
                        else:
                            print(f"Projet ignoré: {project_name} n'est pas un dictionnaire.")
            self.update_project_listbox()
            print("Projets chargés dans l'application:", self.projects)  # Debug message
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erreur lors du chargement des projets: {e}")  # Debug message

    def save_projects(self):
        """
        Sauvegarde les projets dans un fichier JSON.
        """
        print("Sauvegarde des projets...")  # Debug message
        try:
            with open("projects.json", "r") as projects_file:
                projects_data = json.load(projects_file)
        except (FileNotFoundError, json.JSONDecodeError):
            projects_data = {}

        if self.app.auth_manager.is_admin_user(self.app.auth_manager.current_user):
            for project_name, project in self.projects.items():
                projects_data[project_name] = {'priority': project.priority, 'tasks': [task.__dict__ for task in project.tasks]}
        else:
            user_projects = projects_data.get(self.app.auth_manager.current_user, {})
            for project_name, project in self.projects.items():
                user_projects[project_name] = {'priority': project.priority, 'tasks': [task.__dict__ for task in project.tasks]}
            projects_data[self.app.auth_manager.current_user] = user_projects

        with open("projects.json", "w") as projects_file:
            json.dump(projects_data, projects_file, indent=4)
        print("Projets sauvegardés:", json.dumps(projects_data, indent=4))  # Debug message

    def logout(self):
        """
        Sauvegarde les projets et se déconnecte de l'application.
        """
        self.save_projects()  # Ajout de la sauvegarde avant de se déconnecter
        self.app.auth_manager.logout()
