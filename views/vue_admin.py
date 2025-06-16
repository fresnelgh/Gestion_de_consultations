import tkinter as tk
from tkinter import ttk, messagebox
from models.model_utilisateurs import get_all_users, add_user, update_user, delete_user

def launch_admin_view():
    root = tk.Tk()
    root.title("Tableau de bord - Admin")
    root.geometry("1000x600")
    root.configure(bg="#1C1B21")

    selected_user_id = None  # ID de l'utilisateur sélectionné

    # MENU LATERAL
    sidebar = tk.Frame(root, bg="#141316", width=200)
    sidebar.pack(side="left", fill="y")

    tk.Label(sidebar, text="❤️\nJFN-HEALTH", font=("Helvetica", 14, "bold"), fg="#42A07C", bg="#141316", justify="center").pack(pady=30)

    tk.Button(sidebar, text="👤  Personnel", font=("Helvetica", 12), fg="white", bg="#141316", bd=0, anchor="w", activeforeground="#42A07C").pack(fill="x", padx=20, pady=10)

    tk.Button(sidebar, text="↩️  Déconnexion", font=("Helvetica", 12), fg="white", bg="#141316", bd=0, anchor="w", command=root.destroy, activeforeground="#42A07C").pack(side="bottom", fill="x", padx=20, pady=20)

    # ZONE PRINCIPALE
    main_frame = tk.Frame(root, bg="#1C1B21")
    main_frame.pack(side="left", fill="both", expand=True)

    top_bar = tk.Frame(main_frame, bg="#1C1B21")
    top_bar.pack(fill="x", pady=10)

    tk.Label(top_bar, text="Bienvenue M. Fresnel", fg="white", bg="#1C1B21", font=("Helvetica", 12)).pack(side="left", padx=20)
    tk.Label(top_bar, text="👤", fg="white", bg="#1C1B21", font=("Helvetica", 14)).pack(side="left")

    content_frame = tk.Frame(main_frame, bg="#1C1B21")
    content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # FORMULAIRE
    form_box = tk.Frame(content_frame, bg="#18171D", bd=1, relief="solid")
    form_box.pack(side="left", fill="y", padx=10)

    entry_style = {"font": ("Helvetica", 10), "width": 25, "bg": "#1C1B21", "fg": "white", "relief": "flat", "insertbackground": "white"}

    tk.Label(form_box, text="Nom d’utilisateur", fg="white", bg="#18171D").pack(pady=(20, 5))
    entry_nom = tk.Entry(form_box, **entry_style)
    entry_nom.pack(pady=5)

    tk.Label(form_box, text="E-mail", fg="white", bg="#18171D").pack(pady=5)
    entry_email = tk.Entry(form_box, **entry_style)
    entry_email.pack(pady=5)

    tk.Label(form_box, text="Mot de passe", fg="white", bg="#18171D").pack(pady=5)
    entry_password = tk.Entry(form_box, show="*", **entry_style)
    entry_password.pack(pady=5)

    tk.Label(form_box, text="Rôle", fg="white", bg="#18171D").pack(pady=5)
    role_var = tk.StringVar(value="chef_infirmier")
    role_menu = tk.OptionMenu(form_box, role_var, "admin", "chef_infirmier")
    role_menu.config(bg="#2A2A2E", fg="white", relief="flat")
    role_menu.pack(pady=5)

    def enregistrer():
        nom = entry_nom.get()
        email = entry_email.get()
        password = entry_password.get()
        role = role_var.get()
        success, msg = add_user(nom, email, password, role)
        if success:
            messagebox.showinfo("Succès", msg)
            entry_nom.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_password.delete(0, tk.END)
            role_var.set("chef_infirmier")
            charger_utilisateurs()
        else:
            messagebox.showerror("Erreur", msg)

    tk.Button(form_box, text="🗂️  Enregistrer", command=enregistrer, bg="#42A07C", fg="white", width=20, font=("Helvetica", 10, "bold"), relief="flat").pack(pady=20)

    # TABLEAU UTILISATEURS
    table_frame = tk.Frame(content_frame, bg="#1C1B21")
    table_frame.pack(side="right", fill="both", expand=True)

    tk.Label(table_frame, text="📋 Liste du personnel", fg="white", bg="#1C1B21", font=("Helvetica", 12, "bold")).pack(pady=(0, 5))

    columns = ("id", "nom", "email", "role")
    user_table = ttk.Treeview(table_frame, columns=columns, show="headings")
    for col in columns:
        user_table.heading(col, text=col.capitalize())
        user_table.column(col, width=150)
    user_table.pack(expand=True, fill="both", padx=10, pady=10)

    def charger_utilisateurs():
        nonlocal selected_user_id
        selected_user_id = None
        for row in user_table.get_children():
            user_table.delete(row)
        utilisateurs = get_all_users()
        for utilisateur in utilisateurs:
            user_table.insert("", "end", values=utilisateur)

    def remplir_formulaire(event):
        nonlocal selected_user_id
        selected = user_table.focus()
        if not selected:
            return
        values = user_table.item(selected, "values")
        selected_user_id = values[0]
        entry_nom.delete(0, tk.END)
        entry_nom.insert(0, values[1])
        entry_email.delete(0, tk.END)
        entry_email.insert(0, values[2])
        role_var.set(values[3])

    user_table.bind("<<TreeviewSelect>>", remplir_formulaire)

    def modifier():
        if not selected_user_id:
            messagebox.showwarning("Aucun utilisateur", "Veuillez sélectionner un utilisateur.")
            return
        nom = entry_nom.get()
        email = entry_email.get()
        role = role_var.get()
        success, msg = update_user(selected_user_id, nom, email, role)
        if success:
            messagebox.showinfo("Succès", msg)
            entry_nom.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            role_var.set("chef_infirmier")
            charger_utilisateurs()
        else:
            messagebox.showerror("Erreur", msg)

    def supprimer():
        if not selected_user_id:
            messagebox.showwarning("Aucun utilisateur", "Veuillez sélectionner un utilisateur.")
            return
        confirm = messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet utilisateur ?")
        if confirm:
            success, msg = delete_user(selected_user_id)
            if success:
                messagebox.showinfo("Supprimé", msg)
                charger_utilisateurs()
                entry_nom.delete(0, tk.END)
                entry_email.delete(0, tk.END)
                role_var.set("chef_infirmier")
            else:
                messagebox.showerror("Erreur", msg)

    # BOUTONS ACTION
    action_frame = tk.Frame(table_frame, bg="#1C1B21")
    action_frame.pack(pady=5)

    tk.Button(action_frame, text="✏️ Modifier", command=modifier, bg="#42A07C", fg="white", font=("Helvetica", 10, "bold"), width=15).pack(side="left", padx=10)
    tk.Button(action_frame, text="🗑️ Supprimer", command=supprimer, bg="#E64545", fg="white", font=("Helvetica", 10, "bold"), width=15).pack(side="left", padx=10)

    # FOOTER
    tk.Label(root, text="© 2025 JFN-HUI. Tous droits réservés.", fg="white", bg="#1C1B21", font=("Helvetica", 8)).pack(side="bottom", pady=5)

    charger_utilisateurs()
    root.mainloop()
