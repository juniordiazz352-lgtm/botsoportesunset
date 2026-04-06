import sqlite3

def get_ticket_count():
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tickets")
    total = cursor.fetchone()[0]

    conn.close()
    return total
