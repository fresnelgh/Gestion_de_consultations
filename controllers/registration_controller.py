# controllers/registration_controller.py

from models.registration_model import add_pending_user, is_email_pending
from models.model_utilisateurs import get_user_by_email
import smtplib, ssl
from email.message import EmailMessage

# Adresse de l'expéditeur (paramètre fixe)
EMAIL_SENDER = "fresnelktf@gmail.com"
EMAIL_PASSWORD = "pody jqnw ucdq vzoi"

# Fonction appelée depuis la vue
def envoyer_demande_inscription(full_name, email, password, role):
    if not full_name or not email or not password or not role:
        return False, "Tous les champs sont requis."

    # Vérifie si déjà en attente
    if is_email_pending(email):
        return False, "Une demande pour cet e-mail est déjà en attente."

    # Enregistre la demande
    if add_pending_user(full_name, email, password, role):
        # Trouve un chef infirmier existant
        destinataire = get_chef_infirmier_email()
        if destinataire:
            envoyer_mail_validation(destinataire, full_name, email, role)
            return True, "Demande envoyée. En attente de validation."
        else:
            return False, "Aucun chef infirmier trouvé pour valider l'inscription."
    else:
        return False, "Erreur lors de l'enregistrement de la demande."

# Cherche un chef infirmier existant
def get_chef_infirmier_email():
    # Idéalement, retourne le premier chef infirmier actif
    for email_test in ["chef1@example.com", "chef2@example.com"]:
        user = get_user_by_email(email_test)
        if user and user["role"] == "chef_infirmier":
            return user["email"]
    return None

# Envoie un mail au chef infirmier
def envoyer_mail_validation(destinataire_email, nom_demandeur, email_demandeur, role):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Nouvelle demande d’inscription - JFN Health'
        msg['From'] = EMAIL_SENDER
        msg['To'] = destinataire_email

        contenu = f"""
Bonjour,

Une nouvelle demande d'inscription a été faite :

Nom : {nom_demandeur}
Email : {email_demandeur}
Rôle demandé : {role}

Veuillez valider cette demande depuis l'administration JFN.

Merci.
"""
        msg.set_content(contenu)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

    except Exception as e:
        print("Erreur lors de l'envoi de l'email :", e)
