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
CREATE TABLE IF NOT EXISTS ticket_types (
    nombre TEXT PRIMARY KEY,
    emoji TEXT,
    categoria_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    user_id INTEGER,
    channel_id INTEGER,
    tipo TEXT,
    estado TEXT,
    claimed_by INTEGER
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

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    user_id INTEGER,
    channel_id INTEGER,
    claimed_by INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS form_roles (
    formulario TEXT,
    role_id INTEGER
)
""")
