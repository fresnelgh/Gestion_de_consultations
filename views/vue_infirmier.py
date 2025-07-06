import tkinter as tk
from tkinter import ttk, messagebox
from models.model_consultations import get_all_consultations, get_consultations_by_patient
from views.formulaire_consultation import open_consultation_form
from views.vue_infirmier_personnel import build_edit_profile_frame
from fpdf import FPDF
from datetime import datetime


def build_dashboard_frame(parent, user_id, nom_utilisateur):
    for widget in parent.winfo_children():
        widget.destroy()

    # Style configuration
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
                    rowheight=28,
                    font=("Helvetica", 10))
    style.map("Treeview", background=[("selected", "#42A07C")])
    style.configure("Treeview.Heading",
                    background="#42A07C",
                    foreground="white",
                    font=("Helvetica", 10, "bold"),
                    padding=6)

    # Main container
    main_container = tk.Frame(parent, bg="#F5F7FA")
    main_container.pack(fill="both", expand=True, padx=20, pady=20)

    # Header with user info and search
    header = tk.Frame(main_container, bg="#FFFFFF", bd=0, highlightbackground="#E0E0E0", highlightthickness=1)
    header.pack(fill="x", pady=(0, 20))

    user_frame = tk.Frame(header, bg="#FFFFFF")
    user_frame.pack(side="left", padx=20, pady=15)

    tk.Label(user_frame, text=f"👤 {nom_utilisateur}",
             font=("Helvetica", 12, "bold"), fg="#333333", bg="#FFFFFF").pack(anchor="w")
    tk.Label(user_frame, text="Tableau de bord",
             font=("Helvetica", 10), fg="#666666", bg="#FFFFFF").pack(anchor="w")

    search_frame = tk.Frame(header, bg="#FFFFFF")
    search_frame.pack(side="right", padx=20, pady=15)

    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30, font=("Helvetica", 10))
    search_entry.insert(0, "Rechercher un patient...")
    search_entry.pack(side="left", padx=(0, 5))

    def on_search_focus_in(event):
        if search_entry.get() == "Rechercher un patient...":
            search_entry.delete(0, "end")
            search_entry.config(foreground="#333333")

    def on_search_focus_out(event):
        if not search_entry.get():
            search_entry.insert(0, "Rechercher un patient...")
            search_entry.config(foreground="#999999")

    search_entry.bind("<FocusIn>", on_search_focus_in)
    search_entry.bind("<FocusOut>", on_search_focus_out)
    search_entry.config(foreground="#999999")

    search_btn = ttk.Button(search_frame, text="🔍", width=3)
    search_btn.pack(side="left")

    # Content area
    content_frame = tk.Frame(main_container, bg="#F5F7FA")
    content_frame.pack(fill="both", expand=True)

    # Left panel - Recent consultations
    left_panel = tk.Frame(content_frame, bg="#FFFFFF", bd=0, highlightbackground="#E0E0E0", highlightthickness=1)
    left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

    panel_header = tk.Frame(left_panel, bg="#FFFFFF")
    panel_header.pack(fill="x", padx=15, pady=15)

    tk.Label(panel_header, text="Consultations récentes",
             font=("Helvetica", 12, "bold"), fg="#333333", bg="#FFFFFF").pack(side="left")

    def refresh_all_consultations():
        for row in recent_consultations_tree.get_children():
            recent_consultations_tree.delete(row)
        for row in patient_consultations_tree.get_children():
            patient_consultations_tree.delete(row)
        for row in get_all_consultations():
            recent_consultations_tree.insert("", "end", values=row)

    new_consult_btn = ttk.Button(panel_header, text="+ Nouvelle consultation",
                                 command=lambda: open_consultation_form(refresh_all_consultations))
    new_consult_btn.pack(side="right")

    # Treeview for recent consultations
    recent_consultations_tree = ttk.Treeview(left_panel, columns=("date","heure_arrivee", "heure_depart","patient", "symptomes" ,"traitement"),
                                             show="headings")
    for col in ("date","patient", "symptomes", "traitement","heure_arrivee","heure_depart"):
        recent_consultations_tree.heading(col, text=col.capitalize())
        recent_consultations_tree.column(col, width=120, anchor="w")
    recent_consultations_tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    # Right panel - Patient consultations
    right_panel = tk.Frame(content_frame, bg="#FFFFFF", bd=0, highlightbackground="#E0E0E0", highlightthickness=1)
    right_panel.pack(side="left", fill="both", expand=True, padx=(10, 0))

    panel_header = tk.Frame(right_panel, bg="#FFFFFF")
    panel_header.pack(fill="x", padx=15, pady=15)

    patient_label = tk.Label(panel_header, text="Consultations par patient",
                             font=("Helvetica", 12, "bold"), fg="#333333", bg="#FFFFFF")
    patient_label.pack(side="left")

    # Bouton Imprimer rapport
    def export_to_pdf():
        patient_name = search_var.get()
        if not patient_name or patient_name == "Rechercher un patient...":
            messagebox.showwarning("Avertissement", "Veuillez d'abord rechercher un patient")
            return

        consultations = get_consultations_by_patient(patient_name)
        if not consultations:
            messagebox.showwarning("Avertissement", f"Aucune consultation trouvée pour {patient_name}")
            return

        # Création du PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)

        # Titre
        pdf.cell(0, 10, f"Rapport des consultations - {patient_name}", 0, 1, "C")
        pdf.ln(10)

        # Date du rapport
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Généré le : {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, "C")
        pdf.ln(15)

        # En-tête du tableau
        pdf.set_font("Arial", "B", 12)
        pdf.cell(95, 10, "Date", 1, 0, "C")
        pdf.cell(95, 10, "Symptômes/Traitement", 1, 1, "C")
        pdf.set_font("Arial", "", 12)

        # Contenu des consultations
        for consultation in consultations:
            # Formatage pour s'adapter aux colonnes du PDF
            date = consultation[1] if len(consultation) > 1 else "N/A"
            symptomes = consultation[5] if len(consultation) > 2 else "N/A"
            traitement = consultation[6] if len(consultation) > 3 else "N/A"

            # Première ligne avec la date
            pdf.cell(95, 10, str(date), 1, 0, "C")

            # On combine symptômes et traitement dans la même cellule
            details = f"Symptômes: {symptomes}\nTraitement: {traitement}"

            # On utilise une multi_cell pour le texte sur plusieurs lignes
            pdf.multi_cell(95, 10, details, 1, "L")

        # Pied de page
        pdf.ln(10)
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 10, f"Généré par {nom_utilisateur} - JFN-HEALTH", 0, 0, "C")

        # Sauvegarde du fichier
        filename = f"rapport_consultations_{patient_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)

        messagebox.showinfo("Succès", f"Rapport exporté avec succès sous {filename}")

    print_btn = ttk.Button(panel_header, text="📄 Imprimer rapport", command=export_to_pdf)
    print_btn.pack(side="right", padx=10)

    # Treeview for patient consultations
    patient_consultations_tree = ttk.Treeview(right_panel, columns=("nom", "date", "symptomes", "traitement"),
                                              show="headings")
    for col in ("nom", "date", "symptomes", "traitement"):
        patient_consultations_tree.heading(col, text=col.capitalize())
        patient_consultations_tree.column(col, width=120, anchor="w")
    patient_consultations_tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def recherche_patient():
        patient = search_var.get()
        if not patient or patient == "Rechercher un patient...":
            return
        patient_label.config(text=f'Consultations pour "{patient}"')
        for row in patient_consultations_tree.get_children():
            patient_consultations_tree.delete(row)
        for row in get_consultations_by_patient(patient):
            patient_consultations_tree.insert("", "end", values=row)

    search_btn.config(command=recherche_patient)
    search_entry.bind("<Return>", lambda e: recherche_patient())

    # Footer
    footer = tk.Frame(main_container, bg="#F5F7FA")
    footer.pack(fill="x", pady=(10, 0))

    tk.Label(footer, text="© 2025 JFN-HUI. Tous droits réservés.",
             fg="#666666", bg="#F5F7FA", font=("Helvetica", 8)).pack()

    refresh_all_consultations()


def launch_infirmier_view(user_id, nom_utilisateur, email_utilisateur):
    root = tk.Tk()
    root.title("Tableau de bord - Chef Infirmier")

    # Configuration pour le plein écran
    root.attributes('-fullscreen', True)  # Mode plein écran
    # OU pour une fenêtre maximisée mais avec barre de titre :
    # root.state('zoomed')

    # Alternative pour définir la taille de l'écran
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()
    # root.geometry(f"{screen_width}x{screen_height}+0+0")

    root.configure(bg="#F5F7FA")

    # Configure styles
    style = ttk.Style()
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

    # Navigation buttons
    nav_buttons = [
        ("📂 Tableau de bord", lambda: build_dashboard_frame(main_frame, user_id, nom_utilisateur)),
        ("👥 Consultations", lambda: build_dashboard_frame(main_frame, user_id, nom_utilisateur)),
        ("👤 Mon Profil", lambda: build_edit_profile_frame(main_frame, user_id, nom_utilisateur, email_utilisateur)),
        ("↩️ Déconnexion", lambda: logout(root))
    ]

    for text, cmd in nav_buttons:
        btn = ttk.Button(sidebar, text=text, style="Sidebar.TButton", command=cmd)
        btn.pack(fill="x", padx=10, pady=5)

    # Main content area - ajout d'une gestion responsive
    main_frame = tk.Frame(root, bg="#F5F7FA")
    main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    # Ajout d'un gestionnaire d'événement pour le redimensionnement
    def on_resize(event):
        # Ici vous pouvez ajouter du code pour adapter l'UI si nécessaire
        pass

    root.bind('<Configure>', on_resize)

    def logout(root_window):
        from controllers.navigation import open_login_window
        root_window.destroy()
        open_login_window()

    # Initialize with dashboard
    build_dashboard_frame(main_frame, user_id, nom_utilisateur)

    # Bouton pour quitter le mode plein écran (optionnel)
    if root.attributes('-fullscreen'):
        btn_exit_fullscreen = ttk.Button(root, text="✕",
                                         command=lambda: root.attributes('-fullscreen', False),
                                         style="Sidebar.TButton")
        btn_exit_fullscreen.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

    root.mainloop()