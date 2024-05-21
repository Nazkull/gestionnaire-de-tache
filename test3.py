import re
import json
import os

# Nom du fichier JSON pour stocker les utilisateurs
USERS_FILE_NAME = 'users.json'

class User:
    def __init__(self, file_path):
        self.file_path = file_path
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return {}

    def save_users(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.users, file, indent=4)

    def validate_username(self, username):
        if len(username) < 1:
            print("Le nom d'utilisateur ne peut pas être vide.")
            return False
        return True

    def validate_email(self, email):
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(email_regex, email):
            return True
        else:
            print("Format de courriel invalide.")
            return False

    def validate_password(self, password):
        if len(password) < 8:
            print("Le mot de passe doit contenir au moins 8 caractères.")
            return False
        return True

    def sign_up(self):
        print("Inscription :")
        while True:
            username = input("Entrez un nom d'utilisateur: ")
            if self.validate_username(username) and username not in self.users:
                break
            elif username in self.users:
                print("Le nom d'utilisateur existe déjà.")

        while True:
            email = input("Entrez votre courriel: ")
            if self.validate_email(email):
                break

        while True:
            password = input("Entrez un mot de passe: ")
            if self.validate_password(password):
                break

        self.users[username] = {"email": email, "password": password}
        self.save_users()
        print("Compte créé avec succès !")

    def log_in(self):
        print("Connexion :")
        username = input("Entrez votre nom d'utilisateur: ")
        if username in self.users:
            password = input("Entrez votre mot de passe: ")
            if self.users[username]["password"] == password:
                print("Connexion réussie !")
            else:
                print("Mot de passe incorrect.")
        else:
            print("Nom d'utilisateur non trouvé.")

def main():
    # Obtenir le répertoire du script Python
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construire le chemin complet vers le fichier JSON
    users_file_path = os.path.join(script_dir, USERS_FILE_NAME)
    
    user_manager = User(users_file_path)
    while True:
        print("1. Se connecter")
        print("2. S'inscrire")
        choice = input("Choisissez une option (1/2): ")

        if choice == '1':
            user_manager.log_in()
        elif choice == '2':
            user_manager.sign_up()
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
