import tkinter as tk
from project_manager import ProjectManager
from task_manager import TaskManager
from user_manager import UserManager
from calendar_manager import CalendarManager
from admin_manager import AdminManager
from auth_manager import AuthManager

class TaskManagerApp:
    def __init__(self, root):
        """
        Initialisation de l'application de gestion des tâches.
        """
        # Référence à la fenêtre principale Tkinter
        self.root = root
        # Définir le titre de la fenêtre principale
        self.root.title("Task Manager App")
        # Définir les dimensions de la fenêtre principale
        self.root.geometry("1920x1080")

        # Initialisation des différents gestionnaires de l'application
        self.auth_manager = AuthManager(self)
        self.project_manager = ProjectManager(self)
        self.task_manager = TaskManager(self)
        self.user_manager = UserManager(self)
        self.calendar_manager = CalendarManager(self)
        self.admin_manager = AdminManager(self)

        # Créer et afficher l'interface de connexion
        self.auth_manager.create_login_interface()

        # Définir la méthode à appeler lors de la fermeture de la fenêtre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """
        Méthode appelée lors de la fermeture de la fenêtre.
        Sauvegarde les projets et les tâches si un utilisateur est connecté.
        """
        if self.auth_manager.current_user:
            # Sauvegarder les projets en cours
            self.project_manager.save_projects()
            # Sauvegarder les tâches en cours
            self.task_manager.save_tasks()
        # Fermer la fenêtre principale
        self.root.destroy()

if __name__ == "__main__":
    # Créer l'instance de la fenêtre principale Tkinter
    root = tk.Tk()
    # Créer l'instance de l'application de gestion des tâches
    app = TaskManagerApp(root)
    # Lancer la boucle principale de l'application Tkinter
    root.mainloop()
