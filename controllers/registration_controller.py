from models.registration_model import add_pending_user, is_email_pending
from models.model_utilisateurs import get_all_users
import smtplib, ssl
from email.message import EmailMessage
from config.database import get_connection
from models.model_demandes import ajouter_demande

# Adresse de l'expéditeur (paramètre fixe)
EMAIL_SENDER = "fresnelktf@gmail.com"
EMAIL_PASSWORD = "pody jqnw ucdq vzoi"


def envoyer_demande_inscription(full_name, email, password, role):
    if not full_name or not email or not password or not role:
        return False, "Tous les champs sont requis."

    if is_email_pending(email):
        return False, "Une demande pour cet e-mail est déjà en attente."

    if add_pending_user(full_name, email, password, role):
        # Recherche un validateur (chef infirmier ou admin)
        validateur = trouver_validateur()

        if validateur:
            envoyer_mail_validation(validateur['email'], full_name, email, role)
            ajouter_demande(full_name, email, password, role)
            return True, f"Demande envoyée à {validateur['full_name']} pour validation."

        else:
            return False, "Aucun validateur (admin ou chef infirmier) disponible."
    else:
        return False, "Erreur lors de l'enregistrement de la demande."


def trouver_validateur():
    """Recherche un admin ou chef infirmier actif dans la base de données"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Requête pour trouver un admin ou chef infirmier (priorité aux admins)
        cursor.execute("""
            SELECT full_name, email, role 
            FROM users 
            WHERE role IN ('admin', 'chef_infirmier')
            ORDER BY CASE WHEN role = 'admin' THEN 1 ELSE 2 END
            LIMIT 1
        """)

        validateur = cursor.fetchone()
        conn.close()

        return validateur if validateur else None

    except Exception as e:
        print("Erreur recherche validateur:", e)
        return None


def envoyer_mail_validation(destinataire_email, nom_demandeur, email_demandeur, role):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Nouvelle demande d\'inscription - JFN Health'
        msg['From'] = EMAIL_SENDER
        msg['To'] = destinataire_email

        contenu = f"""
Bonjour,

Une nouvelle demande d'inscription nécessite votre validation :

• Nom : {nom_demandeur}
• Email : {email_demandeur} 
• Rôle demandé : {role}

Action requise:
1. Connectez-vous à l'administration JFN
2. Allez dans l'onglet "Demandes"
3. Validez ou rejetez cette demande

Cordialement,
Système de gestion JFN Health
"""
        msg.set_content(contenu)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

    except Exception as e:
        print("Erreur envoi email:", e)