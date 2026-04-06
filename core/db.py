import sqlite3
import json

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# config
cursor.execute("""
CREATE TABLE IF NOT EXISTS config (
    clave TEXT PRIMARY KEY,
    valor TEXT
)
""")

# forms
cursor.execute("""
CREATE TABLE IF NOT EXISTS forms (
    name TEXT PRIMARY KEY,
    questions TEXT,
    channel_id TEXT
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

# tickets
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    channel_id TEXT PRIMARY KEY,
    user_id TEXT,
    type TEXT,
    claimed_by TEXT,
    closed INTEGER
)
""")

conn.commit()
