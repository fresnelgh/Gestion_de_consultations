# views/vue_infirmier_personnel.py

import customtkinter as ctk
from tkinter import messagebox
from models.model_utilisateurs import update_personal_info

def build_edit_profile_frame(root, user_id, current_name, current_email):
    ctk.set_appearance_mode("light")

    for widget in root.winfo_children():
        widget.destroy()

    ctk.CTkLabel(root, text="👤 Modifier mes informations", font=ctk.CTkFont(size=18, weight="bold"), text_color="#000000").pack(pady=(20, 10))

    entry_name = ctk.CTkEntry(root, width=280, placeholder_text="Nom complet")
    entry_name.insert(0, current_name)
    entry_name.pack(pady=10)

    entry_email = ctk.CTkEntry(root, width=280, placeholder_text="Adresse e-mail")
    entry_email.insert(0, current_email)
    entry_email.pack(pady=10)

    entry_password = ctk.CTkEntry(root, width=280, placeholder_text="Nouveau mot de passe (laisser vide si inchangé)", show="*")
    entry_password.pack(pady=10)

    def enregistrer_modification():
        name = entry_name.get().strip()
        email = entry_email.get().strip()
        password = entry_password.get().strip() or None

        if not name or not email:
            messagebox.showwarning("Champs requis", "Veuillez remplir le nom et l'e-mail.")
            return

        success, msg = update_personal_info(user_id, name, email, password)
        if success:
            messagebox.showinfo("Succès", msg)
        else:
            messagebox.showerror("Erreur", msg)

    ctk.CTkButton(root, text="💾 Enregistrer les modifications", command=enregistrer_modification,
                  fg_color="#42A07C", hover_color="#368f6e", width=280).pack(pady=20)


