import smtplib, ssl
from email.message import EmailMessage

EMAIL_SENDER = "fresnelktf@gmail.com"  # à remplacer
EMAIL_PASSWORD = "pody jqnw ucdq vzoi"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


def envoyer_email_demande_au_admin(admin_email, demande_id, full_name, email_utilisateur, role):
    msg = EmailMessage()
    msg['Subject'] = "Demande de création de compte - JFN Health"
    msg['From'] = EMAIL_SENDER
    msg['To'] = admin_email

    corps = f"""
    Bonjour,

    Une nouvelle demande d'inscription a été soumise :

    - Nom : {full_name}
    - Email : {email_utilisateur}
    - Rôle demandé : {role}

    Souhaitez-vous approuver cette demande ?

    ✅ Valider : http://localhost:8000/valider?id={demande_id}
    ❌ Refuser : http://localhost:8000/refuser?id={demande_id}

    JFN Health - Demandes Automatisées
    """

    msg.set_content(corps)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        return True, "Email envoyé avec succès."
    except Exception as e:
        print("Erreur lors de l'envoi de l'email :", e)
        return False, "Échec de l'envoi de l'email."
