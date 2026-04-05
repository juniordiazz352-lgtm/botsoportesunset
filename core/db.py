import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# formularios
cursor.execute("""
CREATE TABLE IF NOT EXISTS formularios (
    nombre TEXT PRIMARY KEY
)
""")

# preguntas
cursor.execute("""
CREATE TABLE IF NOT EXISTS preguntas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    formulario TEXT,
    pregunta TEXT
)
""")

# respuestas
cursor.execute("""
CREATE TABLE IF NOT EXISTS respuestas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    formulario TEXT,
    pregunta TEXT,
    respuesta TEXT
)
""")

# tickets
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    user_id INTEGER,
    channel_id INTEGER
)
""")

# config
cursor.execute("""
CREATE TABLE IF NOT EXISTS config (
    clave TEXT PRIMARY KEY,
    valor TEXT
)
""")

conn.commit()
