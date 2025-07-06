from config.database import get_connection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def ajouter_demande(full_name, email, password, role):
    """Ajoute une demande de création de compte dans la table pending_requests."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pending_requests (full_name, email, password, role)
            VALUES (%s, %s, %s, %s)
        """, (full_name, email, hash_password(password), role))
        conn.commit()
        conn.close()
        return True, "Demande enregistrée avec succès."
    except Exception as e:
        print("Erreur ajout demande :", e)
        return False, "Erreur lors de l'enregistrement de la demande."

def get_all_demandes():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pending_requests ORDER BY id DESC")
        demandes = cursor.fetchall()
        conn.close()
        return demandes
    except Exception as e:
        print("Erreur récupération des demandes :", e)
        return []

def get_demande_by_id(demande_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pending_requests WHERE id = %s", (demande_id,))
        demande = cursor.fetchone()
        conn.close()
        return demande
    except Exception as e:
        print("Erreur récupération demande :", e)
        return None

def supprimer_demande(demande_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pending_requests WHERE id = %s", (demande_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Erreur suppression demande :", e)
        return False
