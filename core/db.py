import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS config (
    clave TEXT PRIMARY KEY,
    valor TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ticket_types (
    nombre TEXT,
    emoji TEXT,
    categoria_id INTEGER
)
""")

conn.commit()
