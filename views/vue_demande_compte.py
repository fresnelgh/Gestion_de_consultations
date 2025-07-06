import tkinter as tk
from tkinter import messagebox
from controllers.controlleur_demandes import traiter_demande_utilisateur
from controllers.navigation import open_login_window  # Import de la fonction de navigation

def open_demande_compte_view(parent_window=None):
    window = tk.Toplevel()
    window.title("Demande de création de compte")
    window.geometry("400x500")  # Augmenté la hauteur pour le nouveau bouton
    window.configure(bg="#1C1B21")

    # Style configuration
    label_style = {"fg": "white", "bg": "#1C1B21", "font": ("Helvetica", 10)}
    entry_style = {"width": 30, "bg": "#2A2A2E", "fg": "white",
                   "relief": "flat", "insertbackground": "white"}
    button_style = {"bg": "#42A07C", "fg": "white",
                   "font": ("Helvetica", 10, "bold"), "width": 25}

    # Titre
    tk.Label(window, text="Demande de compte",
             font=("Helvetica", 14, "bold"),
             fg="white", bg="#1C1B21").pack(pady=20)

    # Champ Nom complet
    tk.Label(window, text="Nom complet", **label_style).pack(anchor="w", padx=30)
    entry_nom = tk.Entry(window, **entry_style)
    entry_nom.pack(pady=5)

    # Champ Email
    tk.Label(window, text="Email", **label_style).pack(anchor="w", padx=30)
    entry_email = tk.Entry(window, **entry_style)
    entry_email.pack(pady=5)

    # Champ Mot de passe
    tk.Label(window, text="Mot de passe", **label_style).pack(anchor="w", padx=30)
    entry_password = tk.Entry(window, show="*", **entry_style)
    entry_password.pack(pady=5)

    # Sélection du rôle
    tk.Label(window, text="Rôle souhaité", **label_style).pack(anchor="w", padx=30)
    role_var = tk.StringVar(value="chef_infirmier")
    tk.OptionMenu(window, role_var, "chef_infirmier").pack(pady=5)

    # Fonction d'envoi
    def envoyer():
        nom = entry_nom.get()
        email = entry_email.get()
        password = entry_password.get()
        role = role_var.get()

        email_admin = "fresnelkt@gmail.com"

        if not nom or not email or not password:
            messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs.")
            return

        success, msg = traiter_demande_utilisateur(nom, email, password, role, email_admin)
        if success:
            messagebox.showinfo("Succès", msg)
            window.destroy()
        else:
            messagebox.showerror("Erreur", msg)

    # Bouton Demander un compte
    btn_demande = tk.Button(window, text="Demander un compte",
                           command=envoyer, **button_style)
    btn_demande.pack(pady=10)

    btn_retour = tk.Button(window, text="Retour à la connexion",
                          command=lambda: [window.destroy(), open_login_window()],
                          bg="#1C1B21", fg="#42A07C",
                          font=("Helvetica", 9, "underline"),
                          relief="flat", bd=0)
    btn_retour.pack(pady=10)

    # Centrer la fenêtre par rapport à la fenêtre parente
    if parent_window:
        window.transient(parent_window)
        window.geometry(f"+{parent_window.winfo_rootx()+50}+{parent_window.winfo_rooty()+50}")

    window.mainloop()