# Importation du module tkinter sous l'alias tk
import tkinter as tk 
# Importation du sous-module messagebox de tkinter pour afficher des boîtes de dialogue
from tkinter import messagebox 

# Création de la fenêtre principale
fenetre = tk.Tk()
# Définition du titre de la fenêtre
fenetre.title("Liste de tâches")

# Création d'une zone pour afficher les tâches
listbox = tk.Listbox(fenetre, font=("Arial",12), selectbackground="black", selectforeground="white")
# Placement de la zone dans la fenêtre avec un espacement de 10 pixels sur les côtés
listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Création d'un champ de texte pour saisir de nouvelles tâches
entry= tk.Entry(fenetre, font=("Arial",12))
# Placement du champ de texte avec un espacement de 5 pixels en haut et en bas et de 10 pixels sur les côtés
entry.pack(pady=5, padx=10)

# Création d'un cadre pour contenir les boutons
frame_boutons = tk.Frame(fenetre)
frame_boutons.pack(pady=5)
rgjrdojgh

# Définition d'une fonction pour ajouter une tâche à la liste
def ajouter_tache():
    tache = entry.get()  # Récupération du texte saisi dans le champ de texte
    if tache:  # Vérification si le champ n'est pas vide
        listbox.insert(tk.END, tache)  # Ajout de la tâche à la fin de la liste
        entry.delete(0,tk.END)  # Effacement du texte dans le champ de texte

# Définition d'une fonction pour supprimer une tâche sélectionnée de la liste
def supprimer_tache():
    index = listbox.curselection()  # Récupération de l'index de la tâche sélectionnée
    if index:  # Vérification si une tâche est sélectionnée
        selection = listbox.get(index)  # Récupération du texte de la tâche sélectionnée
        # Affichage d'une boîte de dialogue de confirmation pour la suppression
        confirmation = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer la tâche '{selection}' ?")
        if confirmation:  # Si l'utilisateur confirme la suppression
            listbox.delete(index)  # Suppression de la tâche de la liste

# Création d'un bouton pour ajouter une tâche
bouton_ajouter = tk.Button(frame_boutons, text ="Ajouter", command=ajouter_tache, font=("Arial",12), bg="black", fg="white", relief="flat", padx=10)
# Placement du bouton à gauche avec un espacement de 5 pixels entre les autres éléments
bouton_ajouter.pack(side=tk.LEFT, padx=5)

# Création d'un bouton pour supprimer une tâche
bouton_supprimer = tk.Button(frame_boutons, text ="Supprimer", command=supprimer_tache, font=("Arial",12), bg="red", fg="white", relief="flat", padx=10)
# Placement du bouton à gauche avec un espacement de 5 pixels entre les autres éléments
bouton_supprimer.pack(side=tk.LEFT, padx=5)

# Lancement de la boucle principale de la fenêtre pour la maintenir ouverte
fenetre.mainloop()
