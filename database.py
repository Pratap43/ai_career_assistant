import sqlite3

conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
)
""")

# History table
cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    username TEXT,
    score REAL,
    job_desc TEXT
)
""")

conn.commit()

def add_user(username, password):
    cursor.execute("INSERT INTO users VALUES (?,?)", (username, password))
    conn.commit()

def login_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return cursor.fetchall()

def save_result(username, score, job_desc):
    cursor.execute("INSERT INTO history VALUES (?,?,?)", (username, score, job_desc))
    conn.commit()

def get_history(username):
    cursor.execute("SELECT * FROM history WHERE username=?", (username,))
    return cursor.fetchall()