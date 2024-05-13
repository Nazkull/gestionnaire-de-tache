# Définir une classe Task
class Task:
    # Constructeur pour la classe Task
    def __init__(self, name, due_date, status="incomplete"):
        # Initialiser les propriétés de la tâche
        self.name = name
        self.due_date = due_date
        self.status = status

# Définir une classe Project
class Project:
    # Constructeur pour la classe Project
    def __init__(self, name):
        # Initialiser le nom du projet
        self.name = name
        # Initialiser la liste des tâches dans le projet
        self.tasks = []

    # Méthode pour ajouter une tâche au projet
    def add_task(self, task):
        self.tasks.append(task)

    # Méthode pour supprimer une tâche du projet
    def remove_task(self, task_name):
        # Utiliser la compréhension de liste pour filtrer la tâche avec le nom donné
        self.tasks = [task for task in self.tasks if task["name"] != task_name]

    # Méthode pour mettre à jour le statut d'une tâche
    def update_task(self, task_name, new_status):
        # Itérer sur la liste des tâches
        for task in self.tasks:
            # Si le nom de la tâche correspond au nom donné
            if task["name"] == task_name:
                # Mettre à jour le statut de la tâche
                task["status"] = new_status
                # Quitter la boucle
                break

# Exemple d'utilisation :
# Créer un nouveau projet avec le nom "Mon Projet"
p = Project("Mon Projet")
# Ajouter deux tâches au projet
p.add_task(Task("Tâche 1", "2023-12-31"))
p.add_task(Task("Tâche 2", "2024-01-07"))
# Afficher la liste des tâches dans le projet
print(p.tasks)
# Supprimer une tâche du projet
p.remove_task("Tâche 1")
# Afficher la liste des tâches mises à jour dans le projet
print(p.tasks)
# Mettre à jour le statut d'une tâche
p.update_task("Tâche 2", "complétée")
# Afficher la liste des tâches mises à jour dans le projet
print(p.tasks)