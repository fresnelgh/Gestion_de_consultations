import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import interface_admin  # doit être dans le même dossier

import smtplib, ssl
import random
from email.message import EmailMessage


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    email = entry_email.get()
    password = entry_password.get()
    if not email or not password:
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
        return
    conn = sqlite3.connect("consultation.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role, password FROM users WHERE email=?", (email,))
    result = cursor.fetchone()
    conn.close()

    if result and result[1] == hash_password(password):
        role = result[0]
        if role == "admin":
            root.destroy()  # ferme la fenêtre de connexion
            interface_admin.launch_interface_admin()  # ouvre interface admin
        else:
            messagebox.showinfo("Info", "Accès réservé à l'administrateur.")
    else:
        messagebox.showerror("Erreur", "Email ou mot de passe invalide.")

def forgot_password():
    def envoyer_code():
        email = entry_email_fp.get()
        if not email:
            messagebox.showwarning("Erreur", "Veuillez entrer un e-mail.")
            return

        conn = sqlite3.connect("consultation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            messagebox.showerror("Erreur", "Aucun utilisateur trouvé avec cet e-mail.")
            return

        code = str(random.randint(100000, 999999))
        send_reset_code(email, code)
        messagebox.showinfo("Code envoyé", "Un code de vérification a été envoyé à votre adresse e-mail.")
        open_reset_window(email, code)

    def open_reset_window(email, sent_code):
        def verifier_code_et_reinitialiser():
            if entry_code.get() != sent_code:
                messagebox.showerror("Erreur", "Code invalide.")
                return
            npass = entry_new.get()
            cpass = entry_confirm.get()
            if npass != cpass or not npass:
                messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
                return
            hashed = hashlib.sha256(npass.encode()).hexdigest()
            conn = sqlite3.connect("consultation.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password=? WHERE email=?", (hashed, email))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Mot de passe mis à jour.")
            window_code.destroy()
            fp_window.destroy()

        window_code = tk.Toplevel(root)
        window_code.title("Vérification")
        window_code.geometry("350x250")
        window_code.configure(bg="#2C2C2C")

        tk.Label(window_code, text="Code reçu par email", bg="#2C2C2C", fg="white").pack(pady=5)
        entry_code = tk.Entry(window_code)
        entry_code.pack()

        tk.Label(window_code, text="Nouveau mot de passe", bg="#2C2C2C", fg="white").pack(pady=5)
        entry_new = tk.Entry(window_code, show="*")
        entry_new.pack()

        tk.Label(window_code, text="Confirmer mot de passe", bg="#2C2C2C", fg="white").pack(pady=5)
        entry_confirm = tk.Entry(window_code, show="*")
        entry_confirm.pack()

        tk.Button(window_code, text="Réinitialiser", command=verifier_code_et_reinitialiser, bg="#42A07C", fg="white").pack(pady=10)

    # Fenêtre de demande d'e-mail
    fp_window = tk.Toplevel(root)
    fp_window.title("Mot de passe oublié")
    fp_window.geometry("300x150")
    fp_window.configure(bg="#2C2C2C")

    tk.Label(fp_window, text="Entrer votre e-mail :", fg="white", bg="#2C2C2C").pack(pady=10)
    entry_email_fp = tk.Entry(fp_window, width=30)
    entry_email_fp.pack()

    tk.Button(fp_window, text="Envoyer le code", command=envoyer_code, bg="#42A07C", fg="white").pack(pady=10)


# À remplacer par ton email et mot de passe d'application
EMAIL_SENDER = "fresnelktf@gmail.com"
EMAIL_PASSWORD = "19042001@Cle1"

def send_reset_code(recipient_email, code):
    msg = EmailMessage()
    msg['Subject'] = 'Code de réinitialisation - JFN Health'
    msg['From'] = EMAIL_SENDER
    msg['To'] = recipient_email
    msg.set_content(f"Voici votre code de réinitialisation : {code}")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)


# ---- Interface de connexion ----
root = tk.Tk()
root.title("Connexion - JFN Health")
root.geometry("400x400")
root.configure(bg="#1C1B21")

# Cadre visuel pour styliser la zone de connexion
frame = tk.Frame(root, bg="#2A2A2E", bd=2, relief="flat")
frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=320)

tk.Label(frame, text="Connexion Admin", font=("Helvetica", 16, "bold"),
         fg="white", bg="#2A2A2E").pack(pady=(20, 10))

tk.Label(frame, text="Email", font=("Helvetica", 10), fg="white", bg="#2A2A2E").pack(anchor="w", padx=30)
entry_email = tk.Entry(frame, width=30, relief="flat", font=("Helvetica", 10),
                       highlightbackground="#42A07C", highlightthickness=1, bg="#1C1B21", fg="white", insertbackground="white")
entry_email.pack(pady=5)

tk.Label(frame, text="Mot de passe", font=("Helvetica", 10), fg="white", bg="#2A2A2E").pack(anchor="w", padx=30)
entry_password = tk.Entry(frame, show="*", width=30, relief="flat", font=("Helvetica", 10),
                          highlightbackground="#42A07C", highlightthickness=1, bg="#1C1B21", fg="white", insertbackground="white")
entry_password.pack(pady=5)

tk.Button(frame, text="Se connecter", bg="#42A07C", fg="white",
          font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5, command=login).pack(pady=15)

tk.Button(frame, text="Mot de passe oublié ?", bg="#2A2A2E", fg="#42A07C",
          font=("Helvetica", 9), relief="flat", borderwidth=0, command=forgot_password).pack()

root.mainloop()






