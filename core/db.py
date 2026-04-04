import sqlite3
import json

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# PANELES
cursor.execute("""
CREATE TABLE IF NOT EXISTS panels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id INTEGER,
    message_id INTEGER,
    data TEXT
)
""")

# CONTADORES
cursor.execute("""
CREATE TABLE IF NOT EXISTS counters (
    categoria_id INTEGER PRIMARY KEY,
    count INTEGER
)
""")

conn.commit()

# ===== CONTADOR =====
def get_ticket_number(categoria_id):
    cursor.execute("SELECT count FROM counters WHERE categoria_id=?", (categoria_id,))
    row = cursor.fetchone()

    if not row:
        cursor.execute("INSERT INTO counters VALUES (?, ?)", (categoria_id, 1))
        conn.commit()
        return 1

    count = row[0] + 1
    cursor.execute("UPDATE counters SET count=? WHERE categoria_id=?", (count, categoria_id))
    conn.commit()

    return count

# ===== PANEL =====
def save_panel(channel_id, message_id, data):
    cursor.execute(
        "INSERT INTO panels (channel_id, message_id, data) VALUES (?, ?, ?)",
        (channel_id, message_id, json.dumps(data))
    )
    conn.commit()

def get_panels():
    cursor.execute("SELECT * FROM panels")
    return cursor.fetchall()
