# views/forgot_password_view.py

import customtkinter as ctk
from tkinter import messagebox
from controllers.password_reset_controller import (
    envoyer_code_par_email,
    reinitialiser_mot_de_passe
)
from PIL import Image
from customtkinter import CTkImage


def go_back_to_login(main_root):
    """Retour à la page de connexion"""
    from views.vue_login import launch_login_window
    main_root.destroy()  # Ferme la fenêtre actuelle
    launch_login_window()  # Ouvre la fenêtre de connexion


def launch_forgot_password_window(main_root):
    """Vue principale pour la réinitialisation de mot de passe"""
    for widget in main_root.winfo_children():
        widget.destroy()

    # Charger l'icône de retour si disponible
    try:
        icon_back = CTkImage(Image.open("assets/icon_back.png"), size=(15, 15))
    except:
        icon_back = None

    # Frame pour le bouton de retour
    top_frame = ctk.CTkFrame(main_root, fg_color="transparent")
    top_frame.pack(fill="x", padx=10, pady=5)

    # Bouton de retour
    ctk.CTkButton(top_frame,
                  text="Retour",
                  command=lambda: go_back_to_login(main_root),
                  image=icon_back,
                  fg_color="transparent",
                  text_color="#42A07C",
                  hover_color="#1C1B21",
                  anchor="w",
                  width=80).pack(side="left")

    # Titre principal
    ctk.CTkLabel(main_root,
                 text="🔐 Réinitialiser le mot de passe",
                 font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

    # Champ email
    ctk.CTkLabel(main_root, text="Adresse e-mail").pack(pady=(10, 0))
    entry_email = ctk.CTkEntry(main_root,
                               width=280,
                               placeholder_text="Entrez votre email")
    entry_email.pack(pady=10)

    # Bouton d'envoi de code
    def envoyer_code():
        email = entry_email.get().strip()
        if not email:
            messagebox.showerror("Erreur", "Veuillez entrer votre email")
            return

        success, msg = envoyer_code_par_email(email)
        if success:
            messagebox.showinfo("Succès", msg)
            launch_code_verification(main_root, email)
        else:
            messagebox.showerror("Erreur", msg)

    ctk.CTkButton(main_root,
                  text="📩 Envoyer le code",
                  command=envoyer_code,
                  fg_color="#42A07C",
                  hover_color="#368f6e").pack(pady=15)


def launch_code_verification(main_root, email):
    """Vue de vérification du code et nouveau mot de passe"""
    for widget in main_root.winfo_children():
        widget.destroy()

    # Charger l'icône de retour si disponible
    try:
        icon_back = CTkImage(Image.open("assets/icon_back.png"), size=(15, 15))
    except:
        icon_back = None

    # Frame pour le bouton de retour
    top_frame = ctk.CTkFrame(main_root, fg_color="transparent")
    top_frame.pack(fill="x", padx=10, pady=5)

    # Bouton de retour
    ctk.CTkButton(top_frame,
                  text="Retour",
                  command=lambda: go_back_to_login(main_root),
                  image=icon_back,
                  fg_color="transparent",
                  text_color="#42A07C",
                  hover_color="#1C1B21",
                  anchor="w",
                  width=80).pack(side="left")

    # Titre principal
    ctk.CTkLabel(main_root,
                 text="✉️ Vérification du code",
                 font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

    # Champ code
    ctk.CTkLabel(main_root, text="Code de vérification").pack()
    entry_code = ctk.CTkEntry(main_root,
                              width=200,
                              placeholder_text="Code à 6 chiffres")
    entry_code.pack(pady=10)

    # Champ nouveau mot de passe
    ctk.CTkLabel(main_root, text="Nouveau mot de passe").pack(pady=(15, 0))
    entry_new = ctk.CTkEntry(main_root,
                             width=280,
                             show="*",
                             placeholder_text="********")
    entry_new.pack(pady=5)

    # Champ confirmation mot de passe
    ctk.CTkLabel(main_root, text="Confirmer le mot de passe").pack(pady=(10, 0))
    entry_confirm = ctk.CTkEntry(main_root,
                                 width=280,
                                 show="*",
                                 placeholder_text="********")
    entry_confirm.pack(pady=5)

    # Bouton de validation
    def valider_reinitialisation():
        code = entry_code.get().strip()
        new = entry_new.get()
        confirm = entry_confirm.get()

        if not code or len(code) != 6:
            messagebox.showerror("Erreur", "Le code doit contenir 6 chiffres")
            return

        if not new or len(new) < 8:
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 8 caractères")
            return

        if new != confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
            return

        success, msg = reinitialiser_mot_de_passe(email, code, new)
        if success:
            messagebox.showinfo("Succès", msg)
            go_back_to_login(main_root)
        else:
            messagebox.showerror("Erreur", msg)

    ctk.CTkButton(main_root,
                  text="✅ Réinitialiser le mot de passe",
                  command=valider_reinitialisation,
                  fg_color="#42A07C",
                  hover_color="#368f6e").pack(pady=20)