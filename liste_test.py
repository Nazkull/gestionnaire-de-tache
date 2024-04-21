import tkinter as tk
from tkinter import messagebox

fenetre = tk.Tk()
fenetre.title("Liste de tâches")

listbox = tk.Listbox(fenetre, font=("Arial",12), selectbackground="black", selectforeground="white")
listbox.pack(pady=10, padx=10, fill=tk.BOTH,expand=True)

entry= tk.Entry(fenetre, font=("Arial",12))
entry.pack(pady=5, padx=10)

frame_boutons = tk.Frame(fenetre)
frame_boutons.pack(pady=5)

def ajouter_tache():
    tache = entry.get()
    if tache:
        listbox.insert(tk.END, tache)
        entry.delete(0,tk.END)


def supprimer_tache() :
    index = listbox.curselection()
    if index:
        selection = listbox.get(index)
        confirmation = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer la tâche' {selection}' ?")
        if confirmation:
            listbox.delete(index)

bouton_ajouter = tk.Button(frame_boutons, text ="Ajouter",command= ajouter_tache, font=("Arial",12),bg="black", fg="white", relief="flat",padx=10)
bouton_ajouter.pack(side=tk.LEFT, padx=5)

bouton_supprimer = tk.Button(frame_boutons, text ="Supprimer",command=supprimer_tache, font=("Arial",12),bg="red", fg="white", relief="flat",padx=10)
bouton_supprimer.pack(side=tk.LEFT, padx=5)

fenetre.mainloop()
