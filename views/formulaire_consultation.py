import tkinter as tk
from tkinter import messagebox
from models.model_consultations import ajouter_consultation

def open_consultation_form():
    form = tk.Toplevel()
    form.title("Nouvelle Consultation")
    form.geometry("400x500")
    form.configure(bg="#1C1B21")

    label_style = {"fg": "white", "bg": "#1C1B21", "font": ("Helvetica", 10)}
    entry_style = {"width": 40, "bg": "#2A2A2E", "fg": "white", "relief": "flat", "insertbackground": "white"}

    tk.Label(form, text="Ajouter une consultation", font=("Helvetica", 14, "bold"), fg="white", bg="#1C1B21").pack(pady=20)

    # Nom du patient
    tk.Label(form, text="Nom du patient", **label_style).pack(anchor="w", padx=20)
    entry_patient = tk.Entry(form, **entry_style)
    entry_patient.pack(padx=20, pady=5)

    # Date
    tk.Label(form, text="Date (AAAA-MM-JJ)", **label_style).pack(anchor="w", padx=20)
    entry_date = tk.Entry(form, **entry_style)
    entry_date.pack(padx=20, pady=5)

    # Symptômes
    tk.Label(form, text="Symptômes", **label_style).pack(anchor="w", padx=20)
    entry_symptomes = tk.Text(form, height=4, width=30, bg="#2A2A2E", fg="white")
    entry_symptomes.pack(padx=20, pady=5)

    # Traitement
    tk.Label(form, text="Traitement", **label_style).pack(anchor="w", padx=20)
    entry_traitement = tk.Text(form, height=4, width=30, bg="#2A2A2E", fg="white")
    entry_traitement.pack(padx=20, pady=5)

    def enregistrer():
        patient = entry_patient.get()
        date = entry_date.get()
        symptomes = entry_symptomes.get("1.0", "end").strip()
        traitement = entry_traitement.get("1.0", "end").strip()

        if not patient or not date:
            messagebox.showwarning("Champs requis", "Le nom du patient et la date sont obligatoires.")
            return

        success, msg = ajouter_consultation(date, patient, symptomes, traitement)
        if success:
            messagebox.showinfo("Succès", msg)
            form.destroy()
        else:
            messagebox.showerror("Erreur", msg)

    tk.Button(form, text="Enregistrer", command=enregistrer, bg="#42A07C", fg="white",
              font=("Helvetica", 10, "bold"), width=20).pack(pady=20)

    form.mainloop()
