import mysql.connector
import hashlib
from config.database import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(full_name, email, password, role):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (full_name, email, password, role)
            VALUES (%s, %s, %s, %s)
        """, (full_name, email, hash_password(password), role))
        conn.commit()
        conn.close()
        return True, "Utilisateur ajouté avec succès."
    except mysql.connector.IntegrityError:
        return False, "Cet e-mail est déjà utilisé."
    except Exception as e:
        print("Erreur ajout utilisateur :", e)
        return False, "Erreur lors de l'ajout de l'utilisateur."

# Vérifier si un utilisateur existe par email
def get_user_by_email(email):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        return user
    except Exception as e:
        print("Erreur lors de la récupération de l'utilisateur :", e)
        return None


def get_all_users():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, email, role FROM users")
        users = cursor.fetchall()
        conn.close()
        return users
    except Exception as e:
        print("Erreur lors du chargement des utilisateurs :", e)
        return []

def update_user_password(email, new_password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        hashed = hash_password(new_password)
        cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed, email))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Erreur update password :", e)
        return False

def update_user(user_id, full_name, email, role):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET full_name=%s, email=%s, role=%s WHERE id=%s
        """, (full_name, email, role, user_id))
        conn.commit()
        conn.close()
        return True, "Utilisateur modifié avec succès."
    except Exception as e:
        print("Erreur modification utilisateur :", e)
        return False, "Erreur lors de la modification."

def delete_user(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
        conn.close()
        return True, "Utilisateur supprimé."
    except Exception as e:
        print("Erreur suppression utilisateur :", e)
        return False, "Erreur lors de la suppression."

def update_personal_info(user_id, new_name, new_email, new_password=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if new_password:
            hashed_pwd = hash_password(new_password)
            cursor.execute("UPDATE users SET full_name=%s, email=%s, password=%s WHERE id=%s",
                           (new_name, new_email, hashed_pwd, user_id))
        else:
            cursor.execute("UPDATE users SET full_name=%s, email=%s WHERE id=%s",
                           (new_name, new_email, user_id))
        conn.commit()
        conn.close()
        return True, "Informations mises à jour avec succès."
    except Exception as e:
        print("Erreur update:", e)
        return False, "Erreur lors de la mise à jour des informations."
