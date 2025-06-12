import tkinter as tk
import sqlite3

def open_consultation_form():
    form = tk.Toplevel()
    form.title("Nouvelle Consultation")
    form.geometry("400x400")
    form.configure(bg="#1C1B21")

    tk.Label(form, text="Ajouter une consultation", font=("Helvetica", 14, "bold"),
             fg="white", bg="#1C1B21").pack(pady=20)

    tk.Label(form, text="Nom du patient", fg="white", bg="#1C1B21").pack(anchor="w", padx=20)
    entry_patient = tk.Entry(form, width=40)
    entry_patient.pack(pady=5)

    tk.Label(form, text="Date (JJ/MM/AAAA)", fg="white", bg="#1C1B21").pack(anchor="w", padx=20)
    entry_date = tk.Entry(form, width=40)
    entry_date.pack(pady=5)

    tk.Label(form, text="Symptômes", fg="white", bg="#1C1B21").pack(anchor="w", padx=20)
    entry_symptomes = tk.Text(form, width=40, height=4)
    entry_symptomes.pack(pady=5)

    tk.Label(form, text="Traitement", fg="white", bg="#1C1B21").pack(anchor="w", padx=20)
    entry_traitement = tk.Text(form, width=40, height=4)
    entry_traitement.pack(pady=5)

    def save_consultation():
        patient = entry_patient.get()
        date = entry_date.get()
        symptomes = entry_symptomes.get("1.0", "end").strip()
        traitement = entry_traitement.get("1.0", "end").strip()

        if patient and date:
            conn = sqlite3.connect("consultations.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO consultations (patient, date, symptomes, traitement)
                VALUES (?, ?, ?, ?)
            """, (patient, date, symptomes, traitement))
            conn.commit()
            conn.close()
            print("Consultation enregistrée.")
            form.destroy()
        else:
            tk.messagebox.showwarning("Champs manquants", "Veuillez remplir le nom du patient et la date.")

    tk.Button(form, text="Enregistrer", bg="#42A07C", fg="white",
              width=20, command=save_consultation).pack(pady=20)
