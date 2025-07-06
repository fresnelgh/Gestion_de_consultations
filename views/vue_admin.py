import tkinter as tk
from tkinter import ttk, messagebox
from models.model_utilisateurs import get_all_users, add_user, update_user, delete_user
from views.vue_admin_demandes import open_admin_demandes_view


def launch_admin_view():
    root = tk.Tk()
    root.title("Tableau de bord - Admin")
    root.geometry("1200x700")
    root.configure(bg="#F5F7FA")

    # Style configuration
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#F5F7FA")
    style.configure("Sidebar.TFrame", background="#1C1B21")
    style.configure("Sidebar.TLabel", background="#1C1B21", foreground="white", font=("Helvetica", 12))
    style.configure("Sidebar.TButton",
                    background="#1C1B21",
                    foreground="white",
                    font=("Helvetica", 11),
                    anchor="w",
                    padding=10)
    style.map("Sidebar.TButton",
              background=[("active", "#2A2A2E")],
              foreground=[("active", "#42A07C")])
    style.configure("Treeview",
                    background="#FFFFFF",
                    foreground="#333333",
                    fieldbackground="#FFFFFF",
                    rowheight=30,
                    font=("Helvetica", 10))
    style.configure("Treeview.Heading",
                    background="#42A07C",
                    foreground="white",
                    font=("Helvetica", 11, "bold"),
                    padding=6)
    style.map('Treeview', background=[('selected', '#A0D6B4')])

    selected_user_id = None

    # Sidebar
    sidebar = ttk.Frame(root, style="Sidebar.TFrame", width=220)
    sidebar.pack(side="left", fill="y")

    # Logo and app name
    logo_frame = ttk.Frame(sidebar, style="Sidebar.TFrame")
    logo_frame.pack(pady=(30, 40), fill="x")

    ttk.Label(logo_frame, text="❤", style="Sidebar.TLabel",
              font=("Helvetica", 24)).pack()
    ttk.Label(logo_frame, text="JFN-HEALTH", style="Sidebar.TLabel",
              font=("Helvetica", 14, "bold"), foreground="#42A07C").pack(pady=(5, 0))

    # Main content area
    main_frame = tk.Frame(root, bg="#F5F7FA")
    main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    content_frame = tk.Frame(main_frame, bg="#F5F7FA")
    content_frame.pack(fill="both", expand=True)

    def afficher_personnel(container):
        nonlocal selected_user_id
        selected_user_id = None

        # Clear container
        for widget in container.winfo_children():
            widget.destroy()

        # Main container with form and table
        main_container = tk.Frame(container, bg="#F5F7FA")
        main_container.pack(fill="both", expand=True)

        # Form frame
        form_frame = tk.Frame(main_container, bg="#FFFFFF", bd=0, highlightbackground="#E0E0E0", highlightthickness=1)
        form_frame.pack(side="left", fill="y", padx=(0, 15), pady=10)

        # Form title
        form_title = tk.Frame(form_frame, bg="#FFFFFF")
        form_title.pack(fill="x", padx=15, pady=15)
        tk.Label(form_title, text="Gestion des utilisateurs",
                 font=("Helvetica", 12, "bold"), fg="#333333", bg="#FFFFFF").pack(side="left")

        def create_form_field(parent, label, placeholder=None, show=None):
            field_frame = tk.Frame(parent, bg="#FFFFFF")
            field_frame.pack(fill="x", padx=15, pady=(0, 15))

            tk.Label(field_frame, text=label, font=("Helvetica", 10),
                     fg="#666666", bg="#FFFFFF").pack(anchor="w")

            entry_var = tk.StringVar()
            entry = ttk.Entry(field_frame, textvariable=entry_var, show=show or "")
            entry.pack(fill="x", ipady=4)

            if placeholder:
                entry.insert(0, placeholder)
                entry.config(foreground="#999999")

                def on_focus_in(event):
                    if entry.get() == placeholder:
                        entry.delete(0, tk.END)
                        entry.config(foreground="#333333")

                def on_focus_out(event):
                    if not entry.get():
                        entry.insert(0, placeholder)
                        entry.config(foreground="#999999")

                entry.bind("<FocusIn>", on_focus_in)
                entry.bind("<FocusOut>", on_focus_out)

            return entry

        # Form fields
        entry_nom = create_form_field(form_frame, "Nom d'utilisateur", "Entrez le nom")
        entry_email = create_form_field(form_frame, "Email", "Entrez l'email")
        entry_password = create_form_field(form_frame, "Mot de passe", "Entrez le mot de passe", show="*")

        # Role selection
        role_frame = tk.Frame(form_frame, bg="#FFFFFF")
        role_frame.pack(fill="x", padx=15, pady=(0, 15))

        tk.Label(role_frame, text="Rôle", font=("Helvetica", 10),
                 fg="#666666", bg="#FFFFFF").pack(anchor="w")

        role_var = tk.StringVar(value="chef_infirmier")
        role_menu = ttk.OptionMenu(role_frame, role_var, "chef_infirmier", "admin", "chef_infirmier")
        role_menu.pack(fill="x")

        # Form buttons
        button_frame = tk.Frame(form_frame, bg="#FFFFFF")
        button_frame.pack(fill="x", padx=15, pady=(10, 15))

        def ajouter_utilisateur():
            nom = entry_nom.get()
            email = entry_email.get()
            password = entry_password.get()
            role = role_var.get()

            if not nom or nom == "Entrez le nom" or not email or email == "Entrez l'email":
                messagebox.showwarning("Champs requis", "Le nom et l'email sont obligatoires.")
                return

            success, msg = add_user(nom, email, password, role)
            if success:
                messagebox.showinfo("Succès", msg)
                charger_utilisateurs()
                # Clear form
                entry_nom.delete(0, tk.END)
                entry_email.delete(0, tk.END)
                entry_password.delete(0, tk.END)
                role_var.set("chef_infirmier")
            else:
                messagebox.showerror("Erreur", msg)

        ttk.Button(button_frame, text="Ajouter", command=ajouter_utilisateur,
                   style="TButton").pack(side="left", padx=(0, 10))

        # Table frame
        table_frame = tk.Frame(main_container, bg="#FFFFFF", bd=0, highlightbackground="#E0E0E0", highlightthickness=1)
        table_frame.pack(side="right", fill="both", expand=True, pady=10)

        # Table header
        table_header = tk.Frame(table_frame, bg="#FFFFFF")
        table_header.pack(fill="x", padx=15, pady=15)

        tk.Label(table_header, text="Liste du personnel",
                 font=("Helvetica", 12, "bold"), fg="#333333", bg="#FFFFFF").pack(side="left")

        # Table
        columns = ("id", "nom", "email", "role")
        user_table = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            user_table.heading(col, text=col.capitalize())
            user_table.column(col, width=120, anchor="w")

        user_table.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Table actions
        action_frame = tk.Frame(table_frame, bg="#FFFFFF")
        action_frame.pack(fill="x", padx=15, pady=(0, 15))

        def modifier_utilisateur():
            if not selected_user_id:
                messagebox.showwarning("Aucun utilisateur", "Veuillez sélectionner un utilisateur.")
                return

            nom = entry_nom.get()
            email = entry_email.get()
            role = role_var.get()

            success, msg = update_user(selected_user_id, nom, email, role)
            if success:
                messagebox.showinfo("Succès", msg)
                charger_utilisateurs()
            else:
                messagebox.showerror("Erreur", msg)

        def supprimer_utilisateur():
            if not selected_user_id:
                messagebox.showwarning("Aucun utilisateur", "Veuillez sélectionner un utilisateur.")
                return

            confirm = messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet utilisateur ?")
            if confirm:
                success, msg = delete_user(selected_user_id)
                if success:
                    messagebox.showinfo("Supprimé", msg)
                    charger_utilisateurs()
                    # Clear form
                    entry_nom.delete(0, tk.END)
                    entry_email.delete(0, tk.END)
                    entry_password.delete(0, tk.END)
                    role_var.set("chef_infirmier")
                else:
                    messagebox.showerror("Erreur", msg)

        ttk.Button(action_frame, text="Modifier", command=modifier_utilisateur,
                   style="TButton").pack(side="left", padx=(0, 10))
        ttk.Button(action_frame, text="Supprimer", command=supprimer_utilisateur).pack(side="left")

        def charger_utilisateurs():
            nonlocal selected_user_id
            selected_user_id = None
            user_table.delete(*user_table.get_children())
            for user in get_all_users():
                user_table.insert("", "end", values=user)

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
        charger_utilisateurs()

    def afficher_demandes(container):
        for widget in container.winfo_children():
            widget.destroy()
        open_admin_demandes_view(container)

    def logout():
        from controllers.navigation import open_login_window
        root.destroy()
        open_login_window()

    # Menu buttons
    menu_buttons = [
        ("👤 Personnel", lambda: afficher_personnel(content_frame)),
        ("📨 Demandes", lambda: afficher_demandes(content_frame)),
        ("↩️ Déconnexion", logout)
    ]

    for text, cmd in menu_buttons:
        btn = ttk.Button(sidebar, text=text, style="Sidebar.TButton", command=cmd)
        btn.pack(fill="x", padx=10, pady=5)

    # Load default view
    afficher_personnel(content_frame)

    root.mainloop()