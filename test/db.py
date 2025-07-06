# db.py

from config import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(100),
            telephone VARCHAR(20)
        )
    """)
    conn.commit()
    conn.close()

def ajouter_contact(nom, telephone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (nom, telephone) VALUES (%s, %s)", (nom, telephone))
    conn.commit()
    conn.close()

def get_contacts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nom, telephone FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    return rows
