import sqlite3
import json

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS panels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id INTEGER,
    message_id INTEGER,
    data TEXT
)
""")

conn.commit()

def save_panel(channel_id, message_id, data):
    cursor.execute(
        "INSERT INTO panels (channel_id, message_id, data) VALUES (?, ?, ?)",
        (channel_id, message_id, json.dumps(data))
    )
    conn.commit()

def get_panels():
    cursor.execute("SELECT * FROM panels")
    rows = cursor.fetchall()

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "channel_id": r[1],
            "message_id": r[2],
            "data": json.loads(r[3])
        })
    return result

def update_panel(panel_id, data):
    cursor.execute(
        "UPDATE panels SET data=? WHERE id=?",
        (json.dumps(data), panel_id)
    )
    conn.commit()

def delete_panel(panel_id):
    cursor.execute("DELETE FROM panels WHERE id=?", (panel_id,))
    conn.commit()

