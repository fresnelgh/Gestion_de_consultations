import mysql.connector

def execute_sql_script(script_path):
    with open(script_path, 'r', encoding='utf-8') as file:
        sql_commands = file.read().split(';')

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # ton mot de passe
    )
    cursor = conn.cursor()
    for command in sql_commands:
        command = command.strip()
        if command:
            cursor.execute(command)
    conn.commit()
    cursor.close()
    conn.close()
