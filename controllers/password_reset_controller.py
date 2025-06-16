# controllers/password_reset_controller.py

import random
import smtplib, ssl
from email.message import EmailMessage
from models.password_reset_model import create_password_reset, is_valid_code, mark_code_as_used
from models.model_utilisateurs import update_user_password, get_user_by_email

# Email d’envoi (Gmail configuré avec mot de passe d'application)
EMAIL_SENDER = "fresnelktf@gmail.com"
EMAIL_PASSWORD = "pody jqnw ucdq vzoi"

# Génère un code à 6 chiffres
def generate_code():
    return str(random.randint(100000, 999999))

# Envoie le code de réinitialisation à l’utilisateur
def envoyer_code_par_email(email):
    user = get_user_by_email(email)
    if not user:
        return False, "Aucun compte trouvé avec cet e-mail."

    code = generate_code()
    if not create_password_reset(email, code):
        return False, "Erreur lors de l’enregistrement du code."

    try:
        msg = EmailMessage()
        msg['Subject'] = "Réinitialisation de mot de passe - JFN Health"
        msg['From'] = EMAIL_SENDER
        msg['To'] = email
        msg.set_content(f"Bonjour,\n\nVoici votre code de vérification : {code}\nCe code est valable 10 minutes.\n\nL'équipe JFN.")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        return True, "Un code vous a été envoyé par e-mail."
    except Exception as e:
        print("Erreur d’envoi email :", e)
        return False, "Erreur lors de l’envoi de l’e-mail."

# Vérifie un code de vérification
def verifier_code(email, code):
    return is_valid_code(email, code)

# Met à jour le mot de passe si le code est valide
def reinitialiser_mot_de_passe(email, code, nouveau_mdp):
    if verifier_code(email, code):
        if update_user_password(email, nouveau_mdp):
            mark_code_as_used(email, code)
            return True, "Mot de passe réinitialisé avec succès."
        else:
            return False, "Erreur lors de la mise à jour du mot de passe."
    else:
        return False, "Code invalide ou expiré."
