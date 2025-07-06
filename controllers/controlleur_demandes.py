from models.model_demandes import ajouter_demande, get_demande_by_id, supprimer_demande
from config.database import get_connection
from mails_utilisateur import envoyer_email_demande_au_admin

def traiter_demande_utilisateur(nom, email, mot_de_passe, role, email_admin):
    """
    Enregistre la demande et envoie un email à l'admin.
    """
    success, message = ajouter_demande(nom, email, mot_de_passe, role)
    if not success:
        return False, message

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM pending_requests WHERE email = %s ORDER BY id DESC LIMIT 1", (email,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return False, "Demande enregistrée, mais impossible de récupérer l'identifiant."

        demande_id = row[0]
        mail_envoye, msg = envoyer_email_demande_au_admin(
            admin_email=email_admin,
            demande_id=demande_id,
            full_name=nom,
            email_utilisateur=email,
            role=role
        )

        if mail_envoye:
            return True, "Demande soumise et email envoyé à l'administrateur."
        else:
            return False, f"Demande soumise mais erreur d'envoi de mail : {msg}"

    except Exception as e:
        print("Erreur traitement demande :", e)
        return False, "Erreur interne lors du traitement de la demande."
