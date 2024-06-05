import tkinter as tk

class AdminManager:
    def __init__(self, app):
        """
        Initialise le gestionnaire d'administration.
        """
        self.app = app

    def create_admin_interface(self):
        """
        Crée l'interface utilisateur pour les administrateurs.
        """
        # Efface les autres cadres et affiche le cadre admin
        self.app.auth_manager.clear_frames()
        self.app.auth_manager.admin_frame.pack()

        # Ajoute un label pour le titre de l'interface admin
        tk.Label(self.app.auth_manager.admin_frame, text="Interface Admin", font=("Helvetica", 16)).pack(pady=10)

        # Ajoute une listbox pour afficher les membres
        self.app.auth_manager.member_listbox = tk.Listbox(self.app.auth_manager.admin_frame, width=50, height=15)
        self.app.auth_manager.member_listbox.pack(pady=10, padx=10)
        self.app.auth_manager.member_listbox.bind("<<ListboxSelect>>", self.app.user_manager.select_member)

        # Ajoute des boutons pour modifier le profil, supprimer un membre et revenir à l'interface de connexion
        tk.Button(self.app.auth_manager.admin_frame, text="Modifier Profil", command=self.app.user_manager.modify_member_profile).pack(pady=5)
        tk.Button(self.app.auth_manager.admin_frame, text="Supprimer Membre", command=self.app.user_manager.delete_member).pack(pady=5)
        tk.Button(self.app.auth_manager.admin_frame, text="Retour", command=self.app.auth_manager.create_login_interface).pack(pady=5)

        # Charge les membres dans la listbox
        self.app.user_manager.load_members()
