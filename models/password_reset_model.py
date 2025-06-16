# models/password_reset_model.py

from config.database import get_connection
from datetime import datetime, timedelta

# Créer une nouvelle demande de réinitialisation
def create_password_reset(email, code):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO password_resets (email, code)
            VALUES (%s, %s)
        """, (email, code))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Erreur insertion reset :", e)
        return False

# Vérifie si un code est valide et actif (non utilisé, pas expiré)
def is_valid_code(email, code):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT created_at, used FROM password_resets
            WHERE email = %s AND code = %s
            ORDER BY created_at DESC LIMIT 1
        """, (email, code))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return False

        created_at, used = row
        if used:
            return False

        now = datetime.now()
        if now - created_at > timedelta(minutes=10):  # code expiré après 10 min
            return False

        return True

    except Exception as e:
        print("Erreur vérification code :", e)
        return False

# Marquer un code comme utilisé
def mark_code_as_used(email, code):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE password_resets SET used = TRUE
            WHERE email = %s AND code = %s
        """, (email, code))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Erreur mise à jour code utilisé :", e)
