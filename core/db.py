import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Tabla de panels
cursor.execute("""
CREATE TABLE IF NOT EXISTS panels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER,
    channel_id INTEGER,
    message_id INTEGER,
    type TEXT
)
""")

# Tabla de formularios
cursor.execute("""
CREATE TABLE IF NOT EXISTS forms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    guild_id INTEGER,
    data TEXT,
    status TEXT
)
""")

conn.commit()


# ===== FUNCIONES =====

def create_form(user_id, guild_id, data):
    cursor.execute(
        "INSERT INTO forms (user_id, guild_id, data, status) VALUES (?, ?, ?, ?)",
        (user_id, guild_id, data, "pending")
    )
    conn.commit()


def get_forms():
    cursor.execute("SELECT * FROM forms")
    return cursor.fetchall()


def update_form_status(form_id, status):
    cursor.execute(
        "UPDATE forms SET status = ? WHERE id = ?",
        (status, form_id)
    )
    conn.commit()
