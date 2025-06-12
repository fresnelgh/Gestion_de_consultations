import sqlite3
conn = sqlite3.connect("consultation.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
