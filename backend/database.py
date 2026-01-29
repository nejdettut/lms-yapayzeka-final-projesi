import os
import sqlite3

# Proje kökündeki data/lms.db kullan (backend'den çalışınca doğru yol)
_db_dir = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(_db_dir, exist_ok=True)
_db_path = os.path.join(_db_dir, "lms.db")

def get_connection():
    conn = sqlite3.connect(_db_path)
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

