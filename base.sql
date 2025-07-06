import mysql.connector
from mysql.connector import Error

def execute_sql_script(sql_file_path):
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # ← vérifie bien ton mot de passe MySQL ici
            autocommit=True
        )
        cursor = conn.cursor()
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        print("✔ Script SQL exécuté avec succès.")
        conn.close()

    except Error as err:
        print("❌ Erreur MySQL :", err)

    except Exception as e:
        print("⚠️ Erreur inconnue :", e)
