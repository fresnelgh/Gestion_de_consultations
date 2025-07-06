# interface.py

import tkinter as tk
from tkinter import messagebox
from db import ajouter_contact, get_contacts

def launch_app():
    root = tk.Tk()
    root.title("Gestion des Contacts (MySQL)")
    root.geometry("400x400")
    root.configure(bg="#1C1B21")

    tk.Label(root, text="Nom", bg="#1C1B21", fg="white").pack()
    entry_nom = tk.Entry(root)
    entry_nom.pack()

    tk.Label(root, text="Téléphone", bg="#1C1B21", fg="white").pack()
    entry_tel = tk.Entry(root)
    entry_tel.pack()

    def ajouter():
        nom = entry_nom.get()
        tel = entry_tel.get()
        if nom and tel:
            ajouter_contact(nom, tel)
            messagebox.showinfo("Succès", "Contact ajouté.")
            entry_nom.delete(0, tk.END)
            entry_tel.delete(0, tk.END)
            afficher_contacts()
        else:
            messagebox.showerror("Erreur", "Tous les champs sont requis.")

    tk.Button(root, text="Ajouter", command=ajouter).pack(pady=10)

    tk.Label(root, text="Liste des contacts", bg="#1C1B21", fg="white").pack(pady=10)
    listbox = tk.Listbox(root, width=50)
    listbox.pack()

    def afficher_contacts():
        listbox.delete(0, tk.END)
        for nom, tel in get_contacts():
            listbox.insert(tk.END, f"{nom} - {tel}")

    afficher_contacts()
    root.mainloop()
