from views.forgot_password_view import launch_forgot_password_window
import tkinter as tk
from tkinter import messagebox
from models.model_utilisateurs import get_user_by_email, hash_password
from views.vue_admin import launch_admin_view
# from views.infirmier_view import launch_infirmier_view  # à créer ensuite
from views.registration_request import launch_registration_request

def launch_login_window():
    root = tk.Tk()
    root.title("Connexion - JFN Health")
    root.geometry("500x500")
    root.configure(bg="#1C1B21")

    frame = tk.Frame(root, bg="#2A2A2E")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=350)

    tk.Label(frame, text="Connexion", font=("Helvetica", 16, "bold"),
             fg="white", bg="#2A2A2E").pack(pady=(20, 10))

    tk.Label(frame, text="Email", fg="white", bg="#2A2A2E").pack(anchor="w", padx=30)
    entry_email = tk.Entry(frame, width=30, relief="flat", font=("Helvetica", 10),
                           bg="#1C1B21", fg="white", insertbackground="white")
    entry_email.pack(pady=5)

    tk.Label(frame, text="Mot de passe", fg="white", bg="#2A2A2E").pack(anchor="w", padx=30)
    entry_password = tk.Entry(frame, show="*", width=30, relief="flat", font=("Helvetica", 10),
                              bg="#1C1B21", fg="white", insertbackground="white")
    entry_password.pack(pady=5)

    def login():
        email = entry_email.get()
        password = entry_password.get()

        if not email or not password:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return

        user = get_user_by_email(email)
        if user and user["password"] == hash_password(password):
            role = user["role"]
            root.destroy()

            if role == "admin":
                launch_admin_view()
            elif role == "chef_infirmier":
                from views.vue_infirmier import launch_infirmier_view
                launch_infirmier_view(user["full_name"])
            else:
                messagebox.showerror("Erreur", f"Rôle non reconnu : {role}")
        else:
            messagebox.showerror("Erreur", "Email ou mot de passe invalide.")

    tk.Button(frame, text="Se connecter", command=login,
              bg="#42A07C", fg="white", font=("Helvetica", 10, "bold")).pack(pady=15)

    # === Bouton d'accès à l'inscription (réservé à l'admin) ===
    def ouvrir_inscription():
        root.destroy()
        launch_admin_view()

    tk.Button(frame, text="➕ Ajouter un utilisateur", command=ouvrir_inscription,
              bg="#1C1B21", fg="#42A07C", relief="flat",
              font=("Helvetica", 9, "underline")).pack()
    tk.Button(frame, text="Demander un compte", command=launch_registration_request,
              bg="#42A07C", fg="white", font=("Helvetica", 10, "bold"), relief="flat").pack(pady=5)
    tk.Button(frame, text="Mot de passe oublié ?", command=launch_forgot_password_window,
              bg="#1C1B21", fg="#42A07C", font=("Helvetica", 9), relief="flat").pack()

    root.mainloop()
