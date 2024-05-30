import json
import tkinter as tk
from tkinter import messagebox, simpledialog

class AuthManager:
    def __init__(self, app):
        self.app = app
        self.current_user = None
        self.is_admin = False

        self.login_frame = tk.Frame(self.app.root)
        self.project_frame = tk.Frame(self.app.root)
        self.task_frame = tk.Frame(self.app.root)
        self.admin_frame = tk.Frame(self.app.root)
        self.profile_frame = tk.Frame(self.app.root)

    def create_login_interface(self):
        self.clear_frames()
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Task Manager App", font=("Helvetica", 16)).pack(pady=10)
        
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)
        self.username_entry.insert(0, "Nom d'utilisateur")

        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, "Mot de passe")

        tk.Button(self.login_frame, text="Se connecter", command=self.login).pack(pady=5)
        tk.Button(self.login_frame, text="S'enregistrer", command=self.register_user).pack(pady=5)

    def clear_frames(self):
        for frame in [self.login_frame, self.project_frame, self.task_frame, self.admin_frame, self.profile_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
            frame.pack_forget()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            with open("database.json", "r") as db_file:
                data = json.load(db_file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if isinstance(data, dict) and username in data and isinstance(data[username], dict) and data[username].get('password') == password:
            self.current_user = username
            self.is_admin = data[username].get('role') == 'admin'
            messagebox.showinfo("Succès", f"Bienvenue, {username}")
            self.app.project_manager.create_project_interface()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = tk.Entry(self.login_frame, show='*')
        confirm_password.pack(pady=5)
        confirm_password.insert(0, "Confirmez le mot de passe")

        def confirm_registration():
            confirm_password_value = confirm_password.get()
            if password != confirm_password_value:
                messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
                return

            try:
                with open("database.json", "r") as db_file:
                    data = json.load(db_file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

            if username in data:
                messagebox.showerror("Erreur", "Le nom d'utilisateur existe déjà")
                return

            data[username] = {'password': password, 'role': 'user'}

            with open("database.json", "w") as db_file:
                json.dump(data, db_file)

            messagebox.showinfo("Succès", "Enregistrement réussi")
            confirm_password.pack_forget()
            confirm_button.pack_forget()

        confirm_button = tk.Button(self.login_frame, text="Confirmer", command=confirm_registration)
        confirm_button.pack(pady=5)

    def logout(self):
        self.current_user = None
        self.is_admin = False
        self.create_login_interface()
