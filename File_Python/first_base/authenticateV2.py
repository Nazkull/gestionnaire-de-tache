import json

def register():
    try:
        with open("database.json", "r") as db_file:
            data = json.load(db_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    username = input("Créez un nom d'utilisateur: ")
    password = input("Créez un mot de passe: ")
    password1 = input("Confirmez le mot de passe: ")

    if password != password1:
        print("Les mots de passe ne correspondent pas")
        return register()
    
    if len(password) <= 6:
        print("Mot de passe trop court, recommencez:")
        return register()

    if username in data:
        print("Le nom d'utilisateur existe déjà")
        return register()

    data[username] = password

    with open("database.json", "w") as db_file:
        json.dump(data, db_file)
    
    print("Bienvenue !")

def access():
    try:
        with open("database.json", "r") as db_file:
            data = json.load(db_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Aucune base de données trouvée. Veuillez vous enregistrer d'abord.")
        return

    username = input("Entrez un nom d'utilisateur: ")
    password = input("Entrez un mot de passe: ")

    if not username or not password:
        print("Le nom d'utilisateur et le mot de passe ne peuvent pas être vides.")
        return

    if username in data and data[username] == password:
        print(f"Bonjour, {username}")
    else:
        print("Nom d'utilisateur ou mot de passe erroné.")

def main():
    while True:
        option = input("1. Se connecter | 2. S'enregistrer: ").strip().lower()
        if option == "1":
            access()
            break
        elif option == "2":
            register()
            break
        else:
            print("Option non valide, veuillez choisir '1. Se connecter' ou '2. S'enregistrer'.")

if __name__ == "__main__":
    main()
