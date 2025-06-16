from config.database import get_connection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Ajouter une demande d'inscription
def add_pending_user(full_name, email, password, role):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pending_users (full_name, email, password, role)
            VALUES (%s, %s, %s, %s)
        """, (full_name, email, hash_password(password), role))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Erreur ajout pending_user :", e)
        return False

# Vérifier si une adresse email est déjà en attente
def is_email_pending(email):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pending_users WHERE email = %s", (email,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print("Erreur vérification pending email :", e)
        return False

# (Optionnel) Récupérer toutes les demandes en attente
def get_all_pending_users():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, email, role FROM pending_users WHERE validated = FALSE")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print("Erreur récupération pending users :", e)
        return []
