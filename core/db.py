import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# config básica
cursor.execute("""
CREATE TABLE IF NOT EXISTS config (
    clave TEXT PRIMARY KEY,
    valor TEXT
)
""")

# formularios
cursor.execute("""
CREATE TABLE IF NOT EXISTS forms (
    name TEXT PRIMARY KEY,
    questions TEXT
)
""")

# respuestas
cursor.execute("""
CREATE TABLE IF NOT EXISTS form_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    form_name TEXT,
    answers TEXT
)
""")

conn.commit()
