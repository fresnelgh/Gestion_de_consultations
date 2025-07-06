# config.py

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",           # Ton utilisateur
        password="",           # Ton mot de passe
        database="contact_db"  # La base que tu auras créée
    )
