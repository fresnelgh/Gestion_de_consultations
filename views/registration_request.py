import customtkinter as ctk
from tkinter import messagebox
from controllers.registration_controller import envoyer_demande_inscription
from controllers.navigation import open_login_window  # Import pour la navigation
from PIL import Image
from customtkinter import CTkImage


def build_registration_request(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Titre
    ctk.CTkLabel(parent_frame,
                 text="Demande d'inscription",
                 font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))

    # === Chargement des icônes ===
    try:
        icon_user = CTkImage(Image.open("assets/icon_user.png"), size=(20, 20))
        icon_email = CTkImage(Image.open("assets/icon_mail.png"), size=(20, 20))
        icon_lock = CTkImage(Image.open("assets/icon_lock.png"), size=(20, 20))
        icon_back = CTkImage(Image.open("assets/icon_back.png"), size=(15, 15))
    except:
        icon_user = icon_email = icon_lock = icon_back = None

    # === Bouton de retour ===
    def retour_connexion():
        parent_frame.master.destroy()  # Ferme la fenêtre actuelle
        open_login_window()  # Ouvre la fenêtre de connexion

    btn_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    btn_frame.pack(fill="x", padx=20, pady=5)

    ctk.CTkButton(btn_frame,
                  text="Retour à la connexion",
                  command=retour_connexion,
                  image=icon_back if icon_back else None,
                  fg_color="transparent",
                  text_color="#42A07C",
                  hover_color="#F0F0F0",
                  anchor="w",
                  width=120).pack(side="left")

    # === CHAMP Nom ===
    nom_box = ctk.CTkFrame(parent_frame, fg_color="transparent")
    nom_box.pack(pady=5)
    if icon_user:
        ctk.CTkLabel(nom_box, image=icon_user, text="").pack(side="left", padx=5)
    entry_nom = ctk.CTkEntry(nom_box,
                             placeholder_text="Nom complet",
                             width=250)
    entry_nom.pack(side="left")

    # === CHAMP Email ===
    email_box = ctk.CTkFrame(parent_frame, fg_color="transparent")
    email_box.pack(pady=5)
    if icon_email:
        ctk.CTkLabel(email_box, image=icon_email, text="").pack(side="left", padx=5)
    entry_email = ctk.CTkEntry(email_box,
                               placeholder_text="Email",
                               width=250)
    entry_email.pack(side="left")

    # === CHAMP Mot de passe ===
    pass_box = ctk.CTkFrame(parent_frame, fg_color="transparent")
    pass_box.pack(pady=5)
    if icon_lock:
        ctk.CTkLabel(pass_box, image=icon_lock, text="").pack(side="left", padx=5)
    entry_password = ctk.CTkEntry(pass_box,
                                  placeholder_text="Mot de passe",
                                  show="*",
                                  width=250)
    entry_password.pack(side="left")

    # === Rôle ===
    role_var = ctk.StringVar(value="chef_infirmier")
    role_menu = ctk.CTkOptionMenu(parent_frame,
                                  variable=role_var,
                                  values=["chef_infirmier", "admin"],
                                  width=250)
    role_menu.pack(pady=10)

    # === Bouton de soumission ===
    def soumettre():
        nom = entry_nom.get()
        email = entry_email.get()
        mot_de_passe = entry_password.get()
        role = role_var.get()

        success, msg = envoyer_demande_inscription(nom, email, mot_de_passe, role)
        if success:
            messagebox.showinfo("Succès", msg)
            entry_nom.delete(0, 'end')
            entry_email.delete(0, 'end')
            entry_password.delete(0, 'end')
        else:
            messagebox.showerror("Erreur", msg)

    ctk.CTkButton(parent_frame,
                  text="Soumettre la demande",
                  command=soumettre,
                  fg_color="#42A07C",
                  hover_color="#368f6e",
                  width=350).pack(pady=20)