import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime

class ToDoListApp:
    def __init__(self, master):
        self.master = master
        master.title("Liste de tâches")

        # Création du calendrier
        self.calendar = Calendar(master, selectmode="day", date_pattern="dd/MM/yyyy")
        self.calendar.pack(pady=10)
        self.calendar.bind("<<CalendarSelected>>", self.date_selectionnee)

        # Création d'une zone pour afficher les tâches
        self.listbox = tk.Listbox(master, font=("Arial", 12), selectbackground="black", selectforeground="white")
        self.listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Création d'un cadre pour saisir une nouvelle tâche avec des heures de début et de fin
        self.entry_frame = tk.Frame(master)
        self.entry_frame.pack(pady=5, padx=10, fill=tk.X)

        self.entry = tk.Entry(self.entry_frame, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.start_time = tk.Entry(self.entry_frame, font=("Arial", 12), width=10)
        self.start_time.insert(0, "HH:MM")
        self.start_time.pack(side=tk.LEFT, padx=5)

        self.end_time = tk.Entry(self.entry_frame, font=("Arial", 12), width=10)
        self.end_time.insert(0, "HH:MM")
        self.end_time.pack(side=tk.LEFT, padx=5)

        # Création d'un cadre pour contenir les boutons
        self.frame_boutons = tk.Frame(master)
        self.frame_boutons.pack(pady=5)

        # Création d'un bouton pour ajouter une tâche
        self.bouton_ajouter = tk.Button(self.frame_boutons, text="Ajouter", command=self.ajouter_tache,
                                        font=("Arial", 12), bg="black", fg="white", relief="flat", padx=10)
        self.bouton_ajouter.pack(side=tk.LEFT, padx=5)

        # Création d'un bouton pour supprimer une tâche
        self.bouton_supprimer = tk.Button(self.frame_boutons, text="Supprimer", command=self.supprimer_tache,
                                          font=("Arial", 12), bg="red", fg="white", relief="flat", padx=10)
        self.bouton_supprimer.pack(side=tk.LEFT, padx=5)

        # Création d'un bouton pour modifier une tâche
        self.bouton_modifier = tk.Button(self.frame_boutons, text="Modifier", command=self.preparer_modification_tache,
                                         font=("Arial", 12), bg="blue", fg="white", relief="flat", padx=10)
        self.bouton_modifier.pack(side=tk.LEFT, padx=5)

        # Dictionnaire pour stocker les tâches par date
        self.taches_par_date = {}

    def ajouter_tache(self):
        # Méthode pour ajouter une tâche à la liste
        tache = self.entry.get()
        start_time = self.start_time.get()
        end_time = self.end_time.get()
        date = self.calendar.get_date()
        if tache and self.valider_heure(start_time) and self.valider_heure(end_time):
            if date not in self.taches_par_date:
                self.taches_par_date[date] = []
            duree = self.calculer_duree(start_time, end_time)
            tache_complet = f"{start_time} - {end_time} ({duree}) : {tache}"
            self.taches_par_date[date].append(tache_complet)
            self.entry.delete(0, tk.END)
            self.start_time.delete(0, tk.END)
            self.end_time.delete(0, tk.END)
            self.start_time.insert(0, "HH:MM")
            self.end_time.insert(0, "HH:MM")
            self.afficher_taches(date)
        else:
            messagebox.showerror("Erreur", "Veuillez entrer une tâche et des heures de début et de fin valides.")

    def supprimer_tache(self):
        # Méthode pour supprimer une tâche sélectionnée de la liste
        index = self.listbox.curselection()
        date = self.calendar.get_date()
        if index:
            selection = self.listbox.get(index)
            confirmation = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer la tâche '{selection}' ?")
            if confirmation:
                self.listbox.delete(index)
                self.taches_par_date[date].remove(selection)
                self.afficher_taches(date)

    def preparer_modification_tache(self):
        # Méthode pour préparer la modification d'une tâche sélectionnée
        index = self.listbox.curselection()
        date = self.calendar.get_date()
        if index:
            selection = self.listbox.get(index)
            tache_texte = selection.split(" : ", 1)[1]
            heures_duree = selection.split(" : ", 1)[0]
            heures = heures_duree.split(" (")[0]
            start_time, end_time = heures.split(" - ")

            # Afficher les valeurs actuelles dans les champs
            self.entry.delete(0, tk.END)
            self.start_time.delete(0, tk.END)
            self.end_time.delete(0, tk.END)
            self.entry.insert(0, tache_texte)
            self.start_time.insert(0, start_time)
            self.end_time.insert(0, end_time)

            # Marquer la tâche pour modification
            self.bouton_ajouter.config(text="Mettre à jour", command=lambda: self.modifier_tache(index, date))

    def modifier_tache(self, index, date):
        # Méthode pour modifier une tâche existante
        tache = self.entry.get()
        start_time = self.start_time.get()
        end_time = self.end_time.get()
        if tache and self.valider_heure(start_time) and self.valider_heure(end_time):
            duree = self.calculer_duree(start_time, end_time)
            tache_complet = f"{start_time} - {end_time} ({duree}) : {tache}"
            self.taches_par_date[date][index[0]] = tache_complet
            self.entry.delete(0, tk.END)
            self.start_time.delete(0, tk.END)
            self.end_time.delete(0, tk.END)
            self.start_time.insert(0, "HH:MM")
            self.end_time.insert(0, "HH:MM")
            self.afficher_taches(date)

            # Réinitialiser le bouton ajouter
            self.bouton_ajouter.config(text="Ajouter", command=self.ajouter_tache)
        else:
            messagebox.showerror("Erreur", "Veuillez entrer une tâche et des heures de début et de fin valides.")

    def afficher_taches(self, date):
        # Méthode pour afficher les tâches pour une date sélectionnée
        self.listbox.delete(0, tk.END)
        duree_totale = 0
        if date in self.taches_par_date:
            for tache in self.taches_par_date[date]:
                self.listbox.insert(tk.END, tache)
                heures_duree = tache.split(" : ", 1)[0]
                heures = heures_duree.split(" (")[0]
                start_time, end_time = heures.split(" - ")
                duree_totale += self.calculer_duree_minutes(start_time, end_time)
        self.listbox.insert(tk.END, f"Durée totale: {self.formater_duree(duree_totale)}")

    def valider_heure(self, heure):
        # Méthode pour valider le format de l'heure (HH:MM)
        try:
            hh, mm = map(int, heure.split(':'))
            return 0 <= hh < 24 and 0 <= mm < 60
        except ValueError:
            return False

    def calculer_duree(self, start_time, end_time):
        # Méthode pour calculer la durée entre start_time et end_time
        fmt = '%H:%M'
        tdelta = datetime.strptime(end_time, fmt) - datetime.strptime(start_time, fmt)
        total_minutes = tdelta.total_seconds() / 60
        heures = int(total_minutes // 60)
        minutes = int(total_minutes % 60)
        return f"{heures}h{minutes}m"

    def calculer_duree_minutes(self, start_time, end_time):
        # Méthode pour calculer la durée en minutes entre start_time et end_time
        fmt = '%H:%M'
        tdelta = datetime.strptime(end_time, fmt) - datetime.strptime(start_time, fmt)
        total_minutes = tdelta.total_seconds() / 60
        return total_minutes

    def formater_duree(self, total_minutes):
        # Méthode pour formater la durée totale en heures et minutes
        heures = int(total_minutes // 60)
        minutes = int(total_minutes % 60)
        return f"{heures}h{minutes}m"

    def date_selectionnee(self, event):
        # Méthode pour afficher les tâches quand une nouvelle date est sélectionnée
        date = self.calendar.get_date()
        self.afficher_taches(date)

def main():
    # Fonction principale pour exécuter l'application
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
