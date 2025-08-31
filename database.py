import sqlite3
import hashlib

DB_NAME = "users.db"

def get_db_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_user_table():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def add_user(username: str, password: str) -> bool:
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users(username, password_hash) VALUES (?, ?)", 
                  (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_credentials(username: str, password: str) -> bool:
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return False
    stored_hash = row[0]
    return stored_hash == hash_password(password)