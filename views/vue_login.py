from views.forgot_password_view import launch_forgot_password_window
from models.model_utilisateurs import get_user_by_email, hash_password
from views.registration_request import build_registration_request
from views.vue_admin import launch_admin_view
from views.vue_infirmier import launch_infirmier_view

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage

def launch_login_window():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    root.title("Connexion - JFN Health")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    try:
        bg_image = Image.open("assets/bg.jpg")
        bg_ctk_image = CTkImage(light_image=bg_image, size=(1200, 960))
        background_label = ctk.CTkLabel(root, image=bg_ctk_image, text="", fg_color="black")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Erreur chargement fond :", e)

    form = ctk.CTkFrame(root, width=720, height=600, corner_radius=0, fg_color="#FFFFFF", border_width=1, border_color="#42A07C")
    form.place(relx=0.3, rely=0.5, anchor="center")
    form.lift()

    ctk.CTkLabel(form, text="Connexion", font=ctk.CTkFont(size=24, weight="bold"), text_color="#000000").pack(pady=(36, 24))

    email_frame = ctk.CTkFrame(form, fg_color="transparent", corner_radius=0)
    email_frame.pack(pady=12)
    try:
        icon_email = CTkImage(Image.open("assets/icon_mail.png"), size=(24, 24))
        ctk.CTkLabel(email_frame, image=icon_email, text="").pack(side="left", padx=12)
    except:
        pass
    entry_email = ctk.CTkEntry(email_frame, placeholder_text="Email", width=240, height=34, corner_radius=0)
    entry_email.pack(side="left")

    pass_frame = ctk.CTkFrame(form, fg_color="transparent", corner_radius=0)
    pass_frame.pack(pady=12)
    try:
        icon_pwd = CTkImage(Image.open("assets/icon_lock.png"), size=(24, 24))
        ctk.CTkLabel(pass_frame, image=icon_pwd, text="").pack(side="left", padx=12)
    except:
        pass
    entry_password = ctk.CTkEntry(pass_frame, placeholder_text="Mot de passe", show="*", width=240, height=34, corner_radius=0)
    entry_password.pack(side="left")

    def login():
        email = entry_email.get()
        password = entry_password.get()
        if not email or not password:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return
        user = get_user_by_email(email)
        if user and user["password"] == hash_password(password):
            root.destroy()
            if user["role"] == "admin":
                launch_admin_view()
            elif user["role"] == "chef_infirmier":
                launch_infirmier_view(user["id"], user["full_name"], user["email"])
            else:
                messagebox.showerror("Erreur", f"Rôle non reconnu : {user['role']}")
        else:
            messagebox.showerror("Erreur", "Email ou mot de passe invalide.")

    ctk.CTkButton(form, text="Se connecter", command=login, width=408, height=42,
                  fg_color="#42A07C", corner_radius=0, hover_color="#368f6e").pack(pady=18)

    ctk.CTkButton(form, text="Demander un compte",
                  command=lambda: build_registration_request(form),
                  fg_color="#42A07C", hover_color="#368f6e", width=264).pack(pady=6)

    ctk.CTkButton(form, text="Mot de passe oublié ?", command=lambda: launch_forgot_password_window(root),
                  fg_color="transparent", text_color="#42A07C", hover_color="#E0E0E0", width=264).pack(pady=6)

    root.mainloop()
