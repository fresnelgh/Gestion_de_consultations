import tkinter as tk
from tkinter import ttk
from form_consultation import open_consultation_form

root = tk.Tk()
root.title("Tableau de bord - Chef Infirmier")
root.geometry("1000x600")
root.configure(bg="#121015")

# Menu latéral
sidebar = tk.Frame(root, bg="#1C1B21", width=200)
sidebar.pack(side="left", fill="y")

tk.Label(sidebar, text="❤️\nJFN-HEALTH", font=("Helvetica", 14, "bold"), fg="#42A07C", bg="#1C1B21", justify="center").pack(pady=30)

menu_font = ("Helvetica", 11)
buttons = [
    ("🗂️  Tableau de board", None),
    ("👥  Consultations", None),
    ("🧑  Personnel", None),
    ("↩️  Déconnexion", root.quit)
]
for text, cmd in buttons:
    tk.Button(sidebar, text=text, font=menu_font, fg="white", bg="#1C1B21", bd=0,
              anchor="w", activebackground="#2A2A2E", activeforeground="#42A07C",
              command=cmd if cmd else lambda: None).pack(fill="x", padx=20, pady=10)

# Partie principale
main_frame = tk.Frame(root, bg="#121015")
main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

# Haut de page : bienvenue et recherche
header = tk.Frame(main_frame, bg="#121015")
header.pack(fill="x")

tk.Label(header, text="Bienvenue M. Bouba", fg="white", bg="#121015", font=("Helvetica", 12)).pack(side="left")

tk.Label(header, text="👤", fg="white", bg="#121015", font=("Helvetica", 14)).pack(side="left", padx=10)

search_frame = tk.Frame(header, bg="#121015")
search_frame.pack(side="right")

search_entry = tk.Entry(search_frame, width=30, font=("Helvetica", 10), fg="white", bg="#2A2A2E",
                        relief="flat", insertbackground="white", highlightbackground="#42A07C", highlightthickness=1)
search_entry.insert(0, "Recherchez un patient")
search_entry.pack(side="left", padx=(0, 5))

search_icon = tk.Label(search_frame, text="🔍", bg="#42A07C", fg="white", font=("Helvetica", 10), width=3)
search_icon.pack(side="left")

# Section consultations
consultation_section = tk.Frame(main_frame, bg="#121015")
consultation_section.pack(fill="both", expand=True, pady=20)

# Bloc gauche – consultations récentes
left_box = tk.Frame(consultation_section, bg="#1C1B21", bd=1, relief="solid")
left_box.pack(side="left", expand=True, fill="both", padx=10)

tk.Label(left_box, text="Consultations récentes", fg="white", bg="#1C1B21", font=("Helvetica", 12, "bold")).pack(pady=10)

tk.Button(left_box, text="+  Nouvelle Consultation", font=("Helvetica", 10, "bold"), bg="#42A07C",
          fg="white", relief="flat", padx=10, pady=5, command=open_consultation_form).pack(pady=5)


tree1 = ttk.Treeview(left_box, columns=("date", "patient", "symptomes", "traitement"), show="headings")
for col in tree1["columns"]:
    tree1.heading(col, text=col.capitalize())
tree1.pack(expand=True, fill="both", padx=10, pady=10)

# Bloc droit – consultations liées au patient
right_box = tk.Frame(consultation_section, bg="#1C1B21", bd=1, relief="solid")
right_box.pack(side="left", expand=True, fill="both", padx=10)

tk.Label(right_box, text='Consultations liées au patient "nom du patient"', fg="white", bg="#1C1B21",
         font=("Helvetica", 12, "bold")).pack(pady=10)

tree2 = ttk.Treeview(right_box, columns=("nom", "date", "symptomes", "traitement"), show="headings")
for col in tree2["columns"]:
    tree2.heading(col, text=col.capitalize())
tree2.pack(expand=True, fill="both", padx=10, pady=10)

# Pied de page
tk.Label(main_frame, text="© 2025 JFN-HUI. Tous droits réservés.", fg="white", bg="#121015", font=("Helvetica", 8)).pack(pady=10)

# Appliquer un style sombre au Treeview
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="#2A2A2E",
                foreground="white",
                fieldbackground="#2A2A2E",
                rowheight=25,
                font=("Helvetica", 10))
style.map('Treeview', background=[('selected', '#42A07C')])

root.mainloop()
