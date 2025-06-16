import tkinter as tk
from tkinter import ttk
from models.model_consultations import get_all_consultations, get_consultations_by_patient
from views.formulaire_consultation import open_consultation_form


def launch_infirmier_view(nom_utilisateur):
    root = tk.Tk()
    root.title("Tableau de bord - Chef Infirmier")
    root.geometry("1000x600")
    root.configure(bg="#121015")

    # MENU LATÉRAL
    sidebar = tk.Frame(root, bg="#1C1B21", width=200)
    sidebar.pack(side="left", fill="y")

    tk.Label(sidebar, text="\u2764\nJFN-HEALTH", font=("Helvetica", 14, "bold"),
             fg="#42A07C", bg="#1C1B21", justify="center").pack(pady=30)

    menu_font = ("Helvetica", 11)
    buttons = [
        ("\ud83d\udcc2  Tableau de board", None),
        ("\ud83d\udc65  Consultations", None),
        ("\ud83e\uddd1  Personnel", None),
        ("\u21a9\ufe0f  Deconnexion", root.quit)
    ]
    for text, cmd in buttons:
        tk.Button(sidebar, text=text, font=menu_font, fg="white", bg="#1C1B21", bd=0,
                  anchor="w", activebackground="#2A2A2E", activeforeground="#42A07C",
                  command=cmd if cmd else lambda: None).pack(fill="x", padx=20, pady=10)

    # ZONE PRINCIPALE
    main_frame = tk.Frame(root, bg="#121015")
    main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    # En-tête
    header = tk.Frame(main_frame, bg="#121015")
    header.pack(fill="x")

    tk.Label(header, text=f"Bienvenue {nom_utilisateur}", fg="white", bg="#121015", font=("Helvetica", 12)).pack(side="left")
    tk.Label(header, text="\ud83d\udc64", fg="white", bg="#121015", font=("Helvetica", 14)).pack(side="left", padx=10)

    search_frame = tk.Frame(header, bg="#121015")
    search_frame.pack(side="right")

    search_entry = tk.Entry(search_frame, width=30, font=("Helvetica", 10), fg="white", bg="#2A2A2E",
                            relief="flat", insertbackground="white", highlightbackground="#42A07C", highlightthickness=1)
    search_entry.insert(0, "Recherchez un patient")
    search_entry.pack(side="left", padx=(0, 5))

    search_icon = tk.Label(search_frame, text="\ud83d\udd0d", bg="#42A07C", fg="white",
                           font=("Helvetica", 10), width=3)
    search_icon.pack(side="left")

    # SECTION CONSULTATIONS
    consultation_section = tk.Frame(main_frame, bg="#121015")
    consultation_section.pack(fill="both", expand=True, pady=20)

    # Bloc gauche : consultations récentes
    left_box = tk.Frame(consultation_section, bg="#1C1B21", bd=1, relief="solid")
    left_box.pack(side="left", expand=True, fill="both", padx=10)

    tk.Label(left_box, text="Consultations récentes", fg="white", bg="#1C1B21",
             font=("Helvetica", 12, "bold")).pack(pady=10)

    tk.Button(left_box, text="+  Nouvelle Consultation", font=("Helvetica", 10, "bold"),
              bg="#42A07C", fg="white", relief="flat", padx=10, pady=5,
              command=open_consultation_form).pack(pady=5)

    tree1 = ttk.Treeview(left_box, columns=("date", "patient", "symptomes", "traitement"), show="headings")
    for col in ("date", "patient", "symptomes", "traitement"):
        tree1.heading(col, text=col.capitalize())
    tree1.pack(expand=True, fill="both", padx=10, pady=10)

    # Bloc droit : consultations liées
    right_box = tk.Frame(consultation_section, bg="#1C1B21", bd=1, relief="solid")
    right_box.pack(side="left", expand=True, fill="both", padx=10)

    tk.Label(right_box, text='Consultations liées au patient "nom du patient"',
             fg="white", bg="#1C1B21", font=("Helvetica", 12, "bold")).pack(pady=10)

    tree2 = ttk.Treeview(right_box, columns=("nom", "date", "symptomes", "traitement"), show="headings")
    for col in ("nom", "date", "symptomes", "traitement"):
        tree2.heading(col, text=col.capitalize())
    tree2.pack(expand=True, fill="both", padx=10, pady=10)

    # FONCTIONS DE CHARGEMENT
    def charger_consultations():
        for row in tree1.get_children():
            tree1.delete(row)
        for row in get_all_consultations():
            tree1.insert("", "end", values=row)

    def recherche_patient():
        patient = search_entry.get()
        if not patient or patient == "Recherchez un patient":
            return
        for row in tree2.get_children():
            tree2.delete(row)
        for row in get_consultations_by_patient(patient):
            tree2.insert("", "end", values=row)

    search_icon.bind("<Button-1>", lambda e: recherche_patient())

    # STYLE TREEVIEW
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#2A2A2E",
                    foreground="white",
                    fieldbackground="#2A2A2E",
                    rowheight=25,
                    font=("Helvetica", 10))
    style.map('Treeview', background=[('selected', '#42A07C')])

    # FOOTER
    tk.Label(main_frame, text="© 2025 JFN-HUI. Tous droits réservés.", fg="white", bg="#121015",
             font=("Helvetica", 8)).pack(pady=10)

    charger_consultations()
    root.mainloop()
