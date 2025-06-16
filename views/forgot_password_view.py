# views/forgot_password_view.py

import tkinter as tk
from tkinter import messagebox
from controllers.password_reset_controller import (
    envoyer_code_par_email,
    reinitialiser_mot_de_passe
)

def launch_forgot_password_window():
    root = tk.Toplevel()
    root.title("Mot de passe oublié")
    root.geometry("400x250")
    root.configure(bg="#1C1B21")

    tk.Label(root, text="🔐 Réinitialiser le mot de passe", font=("Helvetica", 14, "bold"),
             fg="white", bg="#1C1B21").pack(pady=15)

    tk.Label(root, text="Adresse e-mail", fg="white", bg="#1C1B21").pack()
    entry_email = tk.Entry(root, width=30, bg="#2A2A2E", fg="white", insertbackground="white")
    entry_email.pack(pady=5)

    def envoyer_code():
        email = entry_email.get().strip()
        success, msg = envoyer_code_par_email(email)
        if success:
            messagebox.showinfo("Succès", msg)
            root.destroy()
            launch_code_verification(email)
        else:
            messagebox.showerror("Erreur", msg)

    tk.Button(root, text="📩 Envoyer le code", command=envoyer_code,
              bg="#42A07C", fg="white", font=("Helvetica", 10, "bold")).pack(pady=15)

    root.mainloop()


def launch_code_verification(email):
    code_window = tk.Toplevel()
    code_window.title("Code de vérification")
    code_window.geometry("400x350")
    code_window.configure(bg="#1C1B21")

    tk.Label(code_window, text="✉️ Entrez le code reçu", font=("Helvetica", 14, "bold"),
             fg="white", bg="#1C1B21").pack(pady=15)

    tk.Label(code_window, text="Code", fg="white", bg="#1C1B21").pack()
    entry_code = tk.Entry(code_window, width=20, bg="#2A2A2E", fg="white", insertbackground="white")
    entry_code.pack(pady=5)

    tk.Label(code_window, text="Nouveau mot de passe", fg="white", bg="#1C1B21").pack(pady=(15, 0))
    entry_new = tk.Entry(code_window, width=30, show="*", bg="#2A2A2E", fg="white", insertbackground="white")
    entry_new.pack(pady=5)

    tk.Label(code_window, text="Confirmer mot de passe", fg="white", bg="#1C1B21").pack(pady=(10, 0))
    entry_confirm = tk.Entry(code_window, width=30, show="*", bg="#2A2A2E", fg="white", insertbackground="white")
    entry_confirm.pack(pady=5)

    def valider_reinitialisation():
        code = entry_code.get().strip()
        new = entry_new.get()
        confirm = entry_confirm.get()

        if new != confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        success, msg = reinitialiser_mot_de_passe(email, code, new)
        if success:
            messagebox.showinfo("Succès", msg)
            code_window.destroy()
        else:
            messagebox.showerror("Erreur", msg)

    tk.Button(code_window, text="✅ Réinitialiser", command=valider_reinitialisation,
              bg="#42A07C", fg="white", font=("Helvetica", 10, "bold")).pack(pady=20)

    code_window.mainloop()
