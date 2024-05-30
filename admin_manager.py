import tkinter as tk
from tkinter import messagebox

class AdminManager:
    def __init__(self, app):
        self.app = app

    def create_admin_interface(self):
        self.app.auth_manager.clear_frames()
        self.app.auth_manager.admin_frame.pack()

        tk.Label(self.app.auth_manager.admin_frame, text="Admin - Gestion des Membres", font=("Helvetica", 16)).pack(pady=10)

        self.app.auth_manager.member_listbox = tk.Listbox(self.app.auth_manager.admin_frame, width=50, height=15)
        self.app.auth_manager.member_listbox.pack(pady=10, padx=10)
        self.app.auth_manager.member_listbox.bind("<<ListboxSelect>>", self.app.user_manager.select_member)

        tk.Button(self.app.auth_manager.admin_frame, text="Modifier Profil Membre", command=self.app.user_manager.modify_member_profile).pack(pady=5)
        tk.Button(self.app.auth_manager.admin_frame, text="Supprimer Membre", command=self.app.user_manager.delete_member).pack(pady=5)
        tk.Button(self.app.auth_manager.admin_frame, text="Retour", command=self.app.project_manager.create_project_interface).pack(pady=5)

        self.app.user_manager.load_members()
