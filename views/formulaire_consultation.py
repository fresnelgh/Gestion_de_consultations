import tkinter as tk
from tkinter import ttk, messagebox
from models.model_consultations import ajouter_consultation


def open_consultation_form(refresh_callback=None):
    form = tk.Toplevel()
    form.title("Nouvelle Consultation")
    form.geometry("500x750")
    form.configure(bg="#F0F2F5")
    form.resizable(False, False)

    # Style configuration
    style = ttk.Style()
    style.configure("TLabel", background="#F0F2F5", foreground="#333333", font=("Helvetica", 10))
    style.configure("TEntry", fieldbackground="#FFFFFF", foreground="#333333", bordercolor="#CCCCCC", relief="flat")
    style.configure("TButton", font=("Helvetica", 10, "bold"), padding=6)
    style.map("TButton", background=[("active", "#3D8B7D"), ("!disabled", "#42A07C")],
              foreground=[("!disabled", "white")])

    # Header Frame
    header_frame = tk.Frame(form, bg="#42A07C")
    header_frame.pack(fill="x", pady=(0, 20))
    tk.Label(header_frame, text="Ajouter une consultation", font=("Helvetica", 16, "bold"),
             fg="white", bg="#42A07C", padx=20, pady=15).pack()

    # Main Container
    main_frame = tk.Frame(form, bg="#F0F2F5")
    main_frame.pack(padx=30, pady=(0, 20), fill="both", expand=True)

    # Form Fields
    fields = [
        ("Nom du patient", "entry"),
        ("Date (AAAA-MM-JJ)", "entry"),
        ("Heure d'arrivée (HH:MM)", "entry"),
        ("Heure de départ (HH:MM)", "entry"),
        ("Symptômes", "text"),
        ("Traitement", "text"),
        ("Posologie", "text")
    ]

    entries = {}
    for i, (label, field_type) in enumerate(fields):
        frame = tk.Frame(main_frame, bg="#F0F2F5")
        frame.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text=label).pack(anchor="w", padx=(0, 5))

        if field_type == "entry":
            entry = ttk.Entry(frame)
            entry.pack(fill="x", ipady=4)
        else:
            entry = tk.Text(frame, height=4 if label != "Posologie" else 3,
                            bg="white", fg="#333333", relief="solid", bd=1,
                            font=("Helvetica", 10))
            entry.pack(fill="x")

        entries[label.split(" ")[0].lower()] = entry

    # Button Frame
    button_frame = tk.Frame(form, bg="#F0F2F5")
    button_frame.pack(pady=(10, 20))

    def enregistrer():
        data = {
            'patient': entries['nom'].get(),
            'date': entries['date'].get(),
            'heure_arrivee': entries['heure'].get(),
            'heure_depart': entries['heure'].get() if len(entries) > 3 else "",
            'symptomes': entries['symptômes'].get("1.0", "end").strip(),
            'traitement': entries['traitement'].get("1.0", "end").strip(),
            'posologie': entries['posologie'].get("1.0", "end").strip()
        }

        if not data['patient'] or not data['date']:
            messagebox.showwarning("Champs requis", "Le nom du patient et la date sont obligatoires.")
            return

        success, msg = ajouter_consultation(
            data['date'], data['heure_arrivee'], data['heure_depart'],
            data['patient'], data['symptomes'], data['traitement'], data['posologie']
        )

        if success:
            messagebox.showinfo("Succès", "Consultation enregistrée avec succès!")
            form.destroy()
            if refresh_callback:
                refresh_callback()
        else:
            messagebox.showerror("Erreur", msg)

    ttk.Button(button_frame, text="Enregistrer", command=enregistrer, style="TButton").pack(side="left", padx=5)
    ttk.Button(button_frame, text="Annuler", command=form.destroy).pack(side="left", padx=5)

    # Add some polish
    form.bind("<Return>", lambda e: enregistrer())
    form.bind("<Escape>", lambda e: form.destroy())

    # Focus first field
    entries['nom'].focus_set()

    form.mainloop()