import sqlite3

def get_connection():
    conn = sqlite3.connect("data/lms.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_user(name, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email)
    )
    conn.commit()
    conn.close()

