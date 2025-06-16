# views/registration_request.py

import tkinter as tk
from tkinter import messagebox
from controllers.registration_controller import envoyer_demande_inscription

def launch_registration_request():
    root = tk.Tk()
    root.title("Demande d'inscription - JFN Health")
    root.geometry("420x450")
    root.configure(bg="#1C1B21")

    frame = tk.Frame(root, bg="#2A2A2E")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=380)

    tk.Label(frame, text="Demande d'inscription", font=("Helvetica", 14, "bold"),
             fg="white", bg="#2A2A2E").pack(pady=(20, 10))

    # Nom
    tk.Label(frame, text="Nom complet", fg="white", bg="#2A2A2E").pack(anchor="w", padx=30)
    entry_nom = tk.Entry(frame, width=30, bg="#1C1B21", fg="white", relief="flat", insertbackground="white")
    entry_nom.pack(pady=5)

    # Email
    tk.Label(frame, text="Email", fg="white", bg="#2A2A2E").pack(anchor="w", padx=30)
    entry_email = tk.Entry(frame, width=30, bg="#1C1B21", fg="white", relief="flat", insertbackground="white")
    entry_email.pack(pady=5)

    # Mot de passe
    tk.Label(frame, text="Mot de passe", fg="white", bg="#2A2A2E").pack(anchor="w", padx=30)
    entry_password = tk.Entry(frame, width=30, show="*", bg="#1C1B21", fg="white", relief="flat", insertbackground="white")
    entry_password.pack(pady=5)

    # Rôle
    tk.Label(frame, text="Rôle demandé", fg="white", bg="#2A2A2E").pack(anchor="w", padx=30)
    role_var = tk.StringVar(value="chef_infirmier")
    role_menu = tk.OptionMenu(frame, role_var, "chef_infirmier", "admin")
    role_menu.config(bg="#1C1B21", fg="white", relief="flat", highlightbackground="#42A07C")
    role_menu.pack(pady=5)

    # Bouton soumettre
    def soumettre_demande():
        nom = entry_nom.get()
        email = entry_email.get()
        mot_de_passe = entry_password.get()
        role = role_var.get()

        success, message = envoyer_demande_inscription(nom, email, mot_de_passe, role)
        if success:
            messagebox.showinfo("Succès", message)
            root.destroy()
        else:
            messagebox.showerror("Erreur", message)

    tk.Button(frame, text="Soumettre la demande", command=soumettre_demande,
              bg="#42A07C", fg="white", font=("Helvetica", 10, "bold")).pack(pady=20)

    root.mainloop()
