import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Paneles
cursor.execute("""
CREATE TABLE IF NOT EXISTS panels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE,
    tipo TEXT,
    titulo TEXT,
    descripcion TEXT,
    color INTEGER,
    rol_id INTEGER
)
""")

# Botones
cursor.execute("""
CREATE TABLE IF NOT EXISTS panel_buttons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    panel_nombre TEXT,
    label TEXT,
    estilo INTEGER,
    tipo TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    channel_id INTEGER,
    estado TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS config (
    clave TEXT PRIMARY KEY,
    valor TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS preguntas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    formulario TEXT,
    pregunta TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS formularios (
    nombre TEXT PRIMARY KEY
)
""")
