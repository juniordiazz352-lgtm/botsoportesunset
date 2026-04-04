import sqlite3
import json

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# TABLA PANELES
cursor.execute("""
CREATE TABLE IF NOT EXISTS panels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id INTEGER,
    message_id INTEGER,
    data TEXT
)
""")

conn.commit()

# ===== GUARDAR PANEL =====
def save_panel(channel_id, message_id, data):
    cursor.execute(
        "INSERT INTO panels (channel_id, message_id, data) VALUES (?, ?, ?)",
        (channel_id, message_id, json.dumps(data) json.loads(data))
    )
    conn.commit()

# ===== OBTENER =====
def get_panels():
    cursor.execute("SELECT * FROM panels")
    return cursor.fetchall()

# ===== ELIMINAR =====
def delete_panel(panel_id):
    cursor.execute("DELETE FROM panels WHERE id=?", (panel_id,))
    conn.commit()

# ===== ACTUALIZAR =====
def update_panel(panel_id, data):
    cursor.execute("UPDATE panels SET data=? WHERE id=?", json.dumps(data) json.loads(data), panel_id))
    conn.commit()
