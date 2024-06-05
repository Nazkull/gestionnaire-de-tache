# Assurez-vous d'avoir installé tkcalendar : pip install tkcalendar

import tkinter as tk
from tkcalendar import Calendar

class CalendarManager:
    def __init__(self, app):
        """
        Initialise le gestionnaire de calendrier.
        """
        self.app = app

    def create_calendar_interface(self):
        """
        Crée l'interface utilisateur pour le calendrier.
        """
        # Efface les autres cadres et affiche le cadre du calendrier
        self.app.auth_manager.clear_frames()
        self.app.auth_manager.calendar_frame.pack()

        # Ajoute un label pour le titre du calendrier
        tk.Label(self.app.auth_manager.calendar_frame, text="Calendrier", font=("Helvetica", 16)).pack(pady=10)

        # Ajoute le widget Calendar
        self.calendar = Calendar(self.app.auth_manager.calendar_frame, selectmode='day', year=2023, month=5, day=22)
        self.calendar.pack(pady=20)

        # Ajoute un bouton pour revenir à l'interface de connexion
        tk.Button(self.app.auth_manager.calendar_frame, text="Retour", command=self.app.auth_manager.create_login_interface).pack(pady=10)
