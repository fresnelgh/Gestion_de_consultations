from config.database import get_connection

def ajouter_consultation(date, patient, symptomes, traitement):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO consultations (date, patient, symptomes, traitement)
            VALUES (%s, %s, %s, %s)
        """, (date, patient, symptomes, traitement))
        conn.commit()
        conn.close()
        return True, "Consultation ajoutée avec succès."
    except Exception as e:
        print("Erreur ajout consultation :", e)
        return False, "Erreur lors de l'ajout de la consultation."

def get_all_consultations():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date, patient, symptomes, traitement FROM consultations ORDER BY date DESC")
        resultats = cursor.fetchall()
        conn.close()
        return resultats
    except Exception as e:
        print("Erreur récupération consultations :", e)
        return []

def get_consultations_by_patient(nom_patient):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT patient, date, symptomes, traitement
            FROM consultations
            WHERE patient LIKE %s
            ORDER BY date DESC
        """, (f"%{nom_patient}%",))
        resultats = cursor.fetchall()
        conn.close()
        return resultats
    except Exception as e:
        print("Erreur recherche consultations patient :", e)
        return []
