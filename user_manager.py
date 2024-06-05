import json
import tkinter as tk
from tkinter import messagebox, simpledialog

class UserManager:
    def __init__(self, app):
        """
        Initialise le gestionnaire d'utilisateurs.
        """
        self.app = app

    def load_members(self):
        """
        Charge les membres depuis le fichier JSON et les affiche dans la liste des membres.
        """
        try:
            with open("database.json", "r") as db_file:
                data = json.load(db_file)
                for username in data.keys():
                    self.app.auth_manager.member_listbox.insert(tk.END, username)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def select_member(self, event):
        """
        Sélectionne un membre dans la liste des membres et affiche une boîte de dialogue avec les informations du profil sélectionné.
        """
        selection = self.app.auth_manager.member_listbox.curselection()
        if selection:
            member_name = self.app.auth_manager.member_listbox.get(selection[0])
            messagebox.showinfo("Info", f"Profil de {member_name} sélectionné")

    def modify_member_profile(self, member_name=None):
        """
        Modifie le profil d'un membre en demandant un nouveau mot de passe.
        """
        if not member_name:
            selection = self.app.auth_manager.member_listbox.curselection()
            if selection:
                member_name = self.app.auth_manager.member_listbox.get(selection[0])

        if member_name:
            new_password = simpledialog.askstring("Modifier Profil", f"Nouveau mot de passe pour {member_name}:")
            if new_password:
                try:
                    with open("database.json", "r") as db_file:
                        data = json.load(db_file)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = {}

                if member_name in data and isinstance(data[member_name], dict):
                    data[member_name]['password'] = new_password

                    with open("database.json", "w") as db_file:
                        json.dump(data, db_file)

                    messagebox.showinfo("Succès", f"Mot de passe de {member_name} modifié")
                else:
                    messagebox.showerror("Erreur", "Utilisateur non trouvé")

    def delete_member(self):
        """
        Supprime un membre sélectionné de la liste et du fichier JSON.
        """
        selection = self.app.auth_manager.member_listbox.curselection()
        if selection:
            member_name = self.app.auth_manager.member_listbox.get(selection[0])
            confirm = messagebox.askyesno("Supprimer Membre", f"Êtes-vous sûr de vouloir supprimer {member_name}?")
            if confirm:
                try:
                    with open("database.json", "r") as db_file:
                        data = json.load(db_file)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = {}

                if member_name in data and isinstance(data[member_name], dict):
                    del data[member_name]

                    with open("database.json", "w") as db_file:
                        json.dump(data, db_file)

                    self.app.auth_manager.member_listbox.delete(selection[0])
                    messagebox.showinfo("Succès", f"Utilisateur {member_name} supprimé")
                else:
                    messagebox.showerror("Erreur", "Utilisateur non trouvé")

    def modify_profile(self):
        """
        Modifie le profil de l'utilisateur actuel en demandant un nouveau mot de passe.
        """
        new_password = simpledialog.askstring("Modifier Profil", "Nouveau mot de passe:")
        if new_password:
            try:
                with open("database.json", "r") as db_file:
                    data = json.load(db_file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

            if self.app.auth_manager.current_user in data and isinstance(data[self.app.auth_manager.current_user], dict):
                data[self.app.auth_manager.current_user]['password'] = new_password

                with open("database.json", "w") as db_file:
                    json.dump(data, db_file)

                messagebox.showinfo("Succès", "Mot de passe modifié")
            else:
                messagebox.showerror("Erreur", "Utilisateur non trouvé")

    def delete_profile(self):
        """
        Supprime le profil de l'utilisateur actuel après confirmation et le déconnecte de l'application.
        """
        confirm = messagebox.askyesno("Supprimer Profil", "Êtes-vous sûr de vouloir supprimer votre profil?")
        if confirm:
            try:
                with open("database.json", "r") as db_file:
                    data = json.load(db_file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

            if self.app.auth_manager.current_user in data and isinstance(data[self.app.auth_manager.current_user], dict):
                del data[self.app.auth_manager.current_user]

                with open("database.json", "w") as db_file:
                    json.dump(data, db_file)

                self.app.auth_manager.current_user = None
                self.app.auth_manager.create_login_interface()
                messagebox.showinfo("Succès", "Profil supprimé")
            else:
                messagebox.showerror("Erreur", "Utilisateur non trouvé")
