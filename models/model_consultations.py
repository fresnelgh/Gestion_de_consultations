from config.database import get_connection

def ajouter_consultation(date, heure_arrivee, heure_depart, patient, symptomes, traitement, posologie):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO consultations (date, heure_arrivee, heure_depart, patient, symptomes, traitement, posologie)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (date, heure_arrivee, heure_depart, patient, symptomes, traitement, posologie))
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
        cursor.execute("""
            SELECT date, heure_arrivee, heure_depart, patient, symptomes, traitement, posologie
            FROM consultations
            ORDER BY date DESC
        """)
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
            SELECT patient, date, heure_arrivee, heure_depart, symptomes, traitement, posologie
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
