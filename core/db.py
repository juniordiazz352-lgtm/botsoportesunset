import sqlite3
import json
import datetime

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# ===== PANELES =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS panels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id INTEGER,
    message_id INTEGER,
    data TEXT
    id | channel_id | message_id | data
)
""")

# ===== CONTADORES =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS counters (
    categoria_id INTEGER PRIMARY KEY,
    count INTEGER
)
""")

# ===== LOGS =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    action TEXT,
    channel TEXT,
    date TEXT
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

# ===== LOG =====
def add_log(user, action, channel):
    cursor.execute(
        "INSERT INTO logs (user, action, channel, date) VALUES (?, ?, ?, ?)",
        (user, action, channel, str(datetime.datetime.now()))
    )
    conn.commit()

def get_logs():
    cursor.execute("SELECT * FROM logs ORDER BY id DESC")
    return cursor.fetchall()

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

def get_panel(panel_id):
    cursor.execute("SELECT * FROM panels WHERE id=?", (panel_id,))
    row = cursor.fetchone()

    return {
        "id": row[0],
        "channel_id": row[1],
        "message_id": row[2],
        "botones": json.loads(row[3])
    }

def update_panel(panel_id, data):
    cursor.execute(
        "UPDATE panels SET data=? WHERE id=?",
        (json.dumps(data["botones"]), panel_id)
    )
    conn.commit()
