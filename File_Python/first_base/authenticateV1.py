import json

def register():
    db = open("database.json", "r")
    Username = input("Créez un nom d'utilisateur:")
    Password = input("Créez un mot de passe:")
    Password1 = input("Confirmez le mot de passe:")
    d = []
    f = []
    for i in db:
        a,b = i.split(", ")
        b = b.strip()
        d.append(a)
        f.append(b)
    data = dict(zip(d, f))
    print(data)
        
    
    if Password != Password1:
        print("Les mots de passe ne correspondent pas")
        register()
    else:
        if len(Password)<=6:
            print("Mot de passe trop court, recommencez:")
            register()
        elif Username in db:
            print("Le nom d'utilisateur existe déjà")
            register()
        else:
            db = open("database.json", "a")
            db.write(Username+", "+Password+"\n")
            print("Bienvenue !")
            

def access():
    db = open("databse.json","r")
    Username = input("Entrez un nom d'utilisateur:")
    Password = input("Entrez un mot de passe:")
    
    if not len(Username or Password)<1:
        d = []
        f = []
        for i in db:
            a,b = i.split(", ")
            b = b.strip()
            d.append(a)
            f.append(b)
        data = dict(zip(d, f))

        try: 
            if data[Username]:
                try:
                    if Password == data[Username]:
                        print("Bonjour,", Username)
                    
                    else:
                        print("Nom d'utilisateur ou mot de passe éronné.")
                except:
                    print("Nom d'utilisateur ou mot de passe éronné.")
            
            else:
                print("Le mot de passe n'existe pas.")
                
        except:
            print("Erreur de connexion.")
            
def main(option=None):
    option = input("Se connecter | S'enregistrer:")
    if option == "se connecter":
        access()
    else:
        register()

    