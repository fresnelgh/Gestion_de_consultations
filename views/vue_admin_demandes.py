import tkinter as tk
from tkinter import ttk, messagebox
from models.model_demandes import get_all_demandes, get_demande_by_id, supprimer_demande
from models.model_utilisateurs import add_user


def open_admin_demandes_view(parent_frame):
    # Clear the frame
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Configure styles
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#F5F7FA")
    style.configure("TLabel", background="#F5F7FA", foreground="#333333", font=("Helvetica", 10))
    style.configure("TButton", font=("Helvetica", 10), padding=6)
    style.map("TButton",
              background=[("active", "#3D8B7D"), ("!disabled", "#42A07C")],
              foreground=[("!disabled", "white")])
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

    # Main container
    main_container = tk.Frame(parent_frame, bg="#F5F7FA")
    main_container.pack(fill="both", expand=True, padx=20, pady=20)

    # Header
    header_frame = tk.Frame(main_container, bg="#F5F7FA")
    header_frame.pack(fill="x", pady=(0, 20))

    tk.Label(header_frame, text="Demandes de création de compte",
             font=("Helvetica", 16, "bold"), fg="#333333", bg="#F5F7FA").pack(side="left")

    # Table frame
    table_frame = tk.Frame(main_container, bg="#FFFFFF", bd=0, highlightbackground="#E0E0E0", highlightthickness=1)
    table_frame.pack(fill="both", expand=True)

    # Table
    columns = ("id", "nom", "email", "role")
    table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

    # Configure columns
    table.column("id", width=80, anchor="center")
    table.column("nom", width=200, anchor="w")
    table.column("email", width=250, anchor="w")
    table.column("role", width=150, anchor="w")

    for col in columns:
        table.heading(col, text=col.capitalize())

    # Add scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    scrollbar.pack(side="right", fill="y")
    table.configure(yscrollcommand=scrollbar.set)

    table.pack(fill="both", expand=True, padx=15, pady=15)

    def charger_demandes():
        # Clear existing rows
        table.delete(*table.get_children())

        # Load new data
        demandes = get_all_demandes()
        for d in demandes:
            table.insert("", "end", values=(d['id'], d['full_name'], d['email'], d['role']))

    def accepter_demande():
        selected = table.focus()
        if not selected:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner une demande à traiter.")
            return

        values = table.item(selected, "values")
        demande_id, nom, email, role = values

        # Get full demande data
        demande = get_demande_by_id(demande_id)
        if not demande:
            messagebox.showerror("Erreur", "La demande sélectionnée n'existe plus.")
            return

        # Confirm action
        confirm = messagebox.askyesno("Confirmation",
                                      f"Voulez-vous vraiment créer un compte pour {nom} ({email}) comme {role}?")
        if not confirm:
            return

        # Create user account
        success, msg = add_user(nom, email, demande['password'], role)
        if success:
            # Delete the demande
            supprimer_demande(demande_id)
            # Refresh the table
            charger_demandes()
            messagebox.showinfo("Succès", f"Le compte pour {nom} a été créé avec succès.")
        else:
            messagebox.showerror("Erreur", msg)

    def refuser_demande():
        selected = table.focus()
        if not selected:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner une demande à refuser.")
            return

        demande_id, nom, email, _ = table.item(selected, "values")

        # Confirm action
        confirm = messagebox.askyesno("Confirmation",
                                      f"Voulez-vous vraiment refuser la demande de {nom} ({email})?")
        if not confirm:
            return

        # Delete the demande
        if supprimer_demande(demande_id):
            charger_demandes()
            messagebox.showinfo("Succès", "La demande a été refusée et supprimée.")
        else:
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la suppression de la demande.")

    # Button frame
    button_frame = tk.Frame(main_container, bg="#F5F7FA")
    button_frame.pack(fill="x", pady=(15, 0))

    # Action buttons
    ttk.Button(button_frame, text="✅ Accepter", command=accepter_demande,
               style="TButton").pack(side="left", padx=(0, 10))
    ttk.Button(button_frame, text="❌ Refuser", command=refuser_demande).pack(side="left")

    # Load initial data
    charger_demandes()

    # Add keyboard shortcuts
    parent_frame.bind("<Return>", lambda e: accepter_demande())
    parent_frame.bind("<Delete>", lambda e: refuser_demande())